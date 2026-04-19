import os

file_path = '.github/workflows/dotnet-build.yml'
with open(file_path, 'r') as f:
    content = f.read()

content = content.replace("run: dotnet dev-certs https --trust || true", "run: dotnet dev-certs https --trust || echo \"SSL_CERT_DIR=$HOME/.aspnet/dev-certs/trust:/usr/lib/ssl/certs\" >> $GITHUB_ENV")
content = content.replace("run: dotnet --version && dotnet dev-certs https --trust || true", "run: dotnet --version && dotnet dev-certs https --trust || echo \"SSL_CERT_DIR=$HOME/.aspnet/dev-certs/trust:/usr/lib/ssl/certs\" >> $GITHUB_ENV")

with open(file_path, 'w') as f:
    f.write(content)
