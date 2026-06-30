/**
 * InfraGuidAI — Authentication Manager (Cognito)
 * Handles login, signup, token storage, and route guards via AWS Cognito.
 *
 * IMPORTANT: Set these values to match your Cognito User Pool configuration.
 * In production, these come from environment config injected at build time.
 */

const COGNITO_CONFIG = {
  UserPoolId: window.__COGNITO_USER_POOL_ID__ || "us-east-1_XXXXXXXXX",
  ClientId: window.__COGNITO_APP_CLIENT_ID__ || "xxxxxxxxxxxxxxxxxxxxxxxxxx",
  Region: window.__COGNITO_REGION__ || "us-east-1",
};

const AUTH_TOKEN_KEY = "infraguidai_token";
const AUTH_USER_KEY = "infraguidai_user";

/**
 * Lightweight Cognito SRP-free auth using InitiateAuth with USER_PASSWORD_AUTH.
 * No Amplify SDK required — uses direct Cognito API calls via fetch.
 */
class CognitoAuth {
  static get endpoint() {
    return `https://cognito-idp.${COGNITO_CONFIG.Region}.amazonaws.com/`;
  }

  static async _call(action, payload) {
    const response = await fetch(this.endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": `AWSCognitoIdentityProviderService.${action}`,
      },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      const message = data.message || data.Message || data.__type || "Authentication failed";
      throw new Error(message);
    }
    return data;
  }

  static async signUp(name, email, password) {
    // Role is intentionally NOT set here — custom:role is not client-writable.
    // New users default to "user"; admins are promoted out-of-band.
    return await this._call("SignUp", {
      ClientId: COGNITO_CONFIG.ClientId,
      Username: email,
      Password: password,
      UserAttributes: [
        { Name: "email", Value: email },
        { Name: "name", Value: name },
      ],
    });
  }

  static async confirmSignUp(email, code) {
    return await this._call("ConfirmSignUp", {
      ClientId: COGNITO_CONFIG.ClientId,
      Username: email,
      ConfirmationCode: code,
    });
  }

  static async signIn(email, password) {
    const result = await this._call("InitiateAuth", {
      AuthFlow: "USER_PASSWORD_AUTH",
      ClientId: COGNITO_CONFIG.ClientId,
      AuthParameters: {
        USERNAME: email,
        PASSWORD: password,
      },
    });
    return result.AuthenticationResult;
  }

  static async refreshToken(refreshToken) {
    const result = await this._call("InitiateAuth", {
      AuthFlow: "REFRESH_TOKEN_AUTH",
      ClientId: COGNITO_CONFIG.ClientId,
      AuthParameters: {
        REFRESH_TOKEN: refreshToken,
      },
    });
    return result.AuthenticationResult;
  }
}

/**
 * Parse a JWT token payload without verification (for extracting claims client-side).
 */
function parseJwt(token) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

class AuthManager {
  static async safeFetchJson(url, options = {}) {
    const token = this.getToken();
    if (token) {
      if (!options.headers) options.headers = {};
      options.headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(url, options);
    let data;
    try {
      data = await response.json();
    } catch {
      if (!response.ok) {
        throw new Error(`Server error (${response.status}): ${response.statusText || "Unable to complete request"}`);
      }
      throw new Error("Invalid response format received from server.");
    }
    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }
    return data;
  }

  static getToken() {
    return localStorage.getItem(AUTH_TOKEN_KEY);
  }

  static getRefreshToken() {
    return localStorage.getItem("infraguidai_refresh_token");
  }

  static getUser() {
    const raw = localStorage.getItem(AUTH_USER_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  static isLoggedIn() {
    const token = this.getToken();
    if (!token) return false;
    // Check if token is expired
    const claims = parseJwt(token);
    if (!claims || !claims.exp) return false;
    if (Date.now() >= claims.exp * 1000) {
      // Try to refresh silently
      this._tryRefresh();
      return false;
    }
    return true;
  }

  static isAdmin() {
    const user = this.getUser();
    return user && user.role === "admin";
  }

  static saveAuth(idToken, user, refreshToken) {
    localStorage.setItem(AUTH_TOKEN_KEY, idToken);
    localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));
    if (refreshToken) {
      localStorage.setItem("infraguidai_refresh_token", refreshToken);
    }
  }

  static logout() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(AUTH_USER_KEY);
    localStorage.removeItem("infraguidai_refresh_token");
    localStorage.removeItem("infraguid_session_id");
    window.location.href = "/login.html";
  }

  static guardPage() {
    if (!this.isLoggedIn()) {
      window.location.href = "/login.html";
      return false;
    }
    return true;
  }

  static guardAdminPage() {
    if (!this.guardPage()) return false;
    if (!this.isAdmin()) {
      window.location.href = "/";
      return false;
    }
    return true;
  }

  static async login(email, password) {
    const authResult = await CognitoAuth.signIn(email, password);
    const idToken = authResult.IdToken;
    const refreshToken = authResult.RefreshToken;
    const claims = parseJwt(idToken);

    const user = {
      user_id: claims.sub,
      email: claims.email || email,
      name: claims.name || claims["cognito:username"] || email,
      role: claims["custom:role"] || "user",
    };

    this.saveAuth(idToken, user, refreshToken);

    // Sync user to backend database
    try {
      await this.safeFetchJson("/api/auth/sync", { method: "POST" });
    } catch (err) {
      console.warn("User sync failed (non-critical):", err.message);
    }

    return { token: idToken, user };
  }

  static async signup(name, email, password) {
    await CognitoAuth.signUp(name, email, password);
    // Return a pending status — user must confirm their email
    return { status: "confirmation_required", email };
  }

  static async confirmSignup(email, code) {
    await CognitoAuth.confirmSignUp(email, code);
    return { status: "confirmed", email };
  }

  static async _tryRefresh() {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) return;
    try {
      const authResult = await CognitoAuth.refreshToken(refreshToken);
      const idToken = authResult.IdToken;
      const claims = parseJwt(idToken);
      const user = {
        user_id: claims.sub,
        email: claims.email,
        name: claims.name || claims["cognito:username"],
        role: claims["custom:role"] || "user",
      };
      this.saveAuth(idToken, user, refreshToken);
    } catch {
      this.logout();
    }
  }

  static renderUserBlock(container) {
    const user = this.getUser();
    if (!user || !container) return;

    const initials = user.name
      .split(" ")
      .map((w) => w[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);

    container.innerHTML = `
      <div class="user-avatar">${escapeHtml(initials)}</div>
      <div class="user-info">
        <span class="user-name">${escapeHtml(user.name)}</span>
        <span class="user-role">${escapeHtml(user.role)}</span>
      </div>
      <button class="btn-logout" id="logoutBtn" title="Logout">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
      </button>
    `;

    container.querySelector("#logoutBtn").addEventListener("click", () => {
      AuthManager.logout();
    });
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[char]);
}
