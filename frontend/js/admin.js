/* InfraGuidAI — Admin Controller */

// Admin auth guard
if (!AuthManager.guardAdminPage()) {
  throw new Error("Not authorized");
}

// Render user block
AuthManager.renderUserBlock(document.getElementById("userBlock"));

// DOM references
const healthStatus = document.getElementById("healthStatus");
const alertBox = document.getElementById("alert");
const docCount = document.getElementById("docCount");
const chunkCount = document.getElementById("chunkCount");
const vectorChunkCount = document.getElementById("vectorChunkCount");
const lastIngestion = document.getElementById("lastIngestion");
const documentsBody = document.getElementById("documentsBody");
const chunks = document.getElementById("chunks");
const refreshButton = document.getElementById("refreshButton");
const ingestButton = document.getElementById("ingestButton");

// Upload DOM references
const uploadDocButton = document.getElementById("uploadDocButton");
const fileInput = document.getElementById("fileInput");

function showAlert(message) {
  alertBox.textContent = message;
  alertBox.hidden = !message;
}

function setHealth(ok, text) {
  healthStatus.textContent = text;
  healthStatus.className = `status-pill ${ok ? "ok" : "fail"}`;
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    setHealth(response.ok, response.ok ? "Healthy" : "Unhealthy");
  } catch {
    setHealth(false, "Offline");
  }
}

async function loadStats() {
  const data = await AuthManager.safeFetchJson("/api/admin/stats");
  docCount.textContent = data.documents;
  chunkCount.textContent = data.chunks;
  vectorChunkCount.textContent = data.vector_chunks;
  lastIngestion.textContent = data.last_ingestion
    ? new Date(data.last_ingestion).toLocaleString()
    : "Never";
}

async function loadDocuments() {
  const data = await AuthManager.safeFetchJson("/api/admin/documents");
  documentsBody.innerHTML = "";
  for (const doc of data) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${escapeHtml(doc.title)}</td>
      <td>${escapeHtml(doc.category)}</td>
      <td>${escapeHtml(doc.path)}</td>
      <td>${escapeHtml(doc.chunk_count)}</td>
      <td>${escapeHtml(doc.owner || "")}</td>
    `;
    documentsBody.appendChild(row);
  }
}

async function loadChunks() {
  const data = await AuthManager.safeFetchJson("/api/admin/chunks?limit=20");
  chunks.innerHTML = "";
  for (const item of data.chunks) {
    const node = document.createElement("div");
    node.className = "panel chunk";
    node.innerHTML = `
      <strong>${escapeHtml(item.metadata.title || item.id)}</strong>
      <div>${escapeHtml(item.metadata.source_path || "")}</div>
      <pre>${escapeHtml(item.preview)}</pre>
    `;
    chunks.appendChild(node);
  }
}

async function refresh() {
  showAlert("");
  try {
    await checkHealth();
    await Promise.all([loadStats(), loadDocuments(), loadChunks()]);
  } catch (error) {
    showAlert(error.message);
  }
}

async function ingest() {
  ingestButton.disabled = true;
  showAlert(
    "Ingestion started. This can take several minutes because embeddings are generated through Bedrock."
  );
  try {
    const data = await AuthManager.safeFetchJson("/api/admin/ingest", { method: "POST" });
    showAlert(
      `Ingestion ${data.status}: ${data.documents_processed || 0} documents, ${data.chunks_created || 0} chunks.`
    );
    await refresh();
  } catch (error) {
    showAlert(error.message);
  } finally {
    ingestButton.disabled = false;
  }
}

// Upload handlers
uploadDocButton.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", async (e) => {
  if (e.target.files && e.target.files.length > 0) {
    const file = e.target.files[0];
    if (!file.name.endsWith(".md")) {
      showAlert("Error: Only Markdown (.md) files are supported.");
      fileInput.value = "";
      return;
    }
    
    try {
      uploadDocButton.disabled = true;
      showAlert(`Uploading ${file.name}...`);
      
      const formData = new FormData();
      formData.append("file", file);
      
      const data = await AuthManager.safeFetchJson("/api/admin/upload", {
        method: "POST",
        body: formData
      });
      
      showAlert(`Uploaded successfully: ${data.filename}`);
      fileInput.value = "";
      await refresh();
    } catch (error) {
      showAlert(error.message || "Failed to upload file.");
    } finally {
      uploadDocButton.disabled = false;
    }
  }
});

refreshButton.addEventListener("click", refresh);
ingestButton.addEventListener("click", ingest);
refresh();
setInterval(checkHealth, 30000);
