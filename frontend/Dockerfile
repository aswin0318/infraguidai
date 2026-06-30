# Static frontend served by nginx. Build context is the repo root.
FROM nginx:alpine

# Static assets + SPA/API-proxy nginx config.
COPY frontend/ /usr/share/nginx/html/
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# The Dockerfile and nginx.conf live under the html root after COPY; drop them.
RUN rm -f /usr/share/nginx/html/Dockerfile /usr/share/nginx/html/nginx.conf

EXPOSE 80
