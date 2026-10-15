FROM nginx:1.30.6-alpine3.24-slim
COPY --chown=101:101 app/index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/nginx.conf
RUN nginx -t
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8080/"]
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
