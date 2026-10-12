@AGENTS.md

# Deploy (Gemini và Claude dùng chung một cách)
- Remote `origin` và `REPO_URL` trong `scripts/deploy.sh` dùng SSH (`git@github.com:itachi2601/thachlab.git`), khoá `~/.ssh/id_ed25519_github` đã nạp vào ssh-agent/Keychain nên push không bị hỏi mật khẩu.
- Deploy chạy trên Mac, ngoài sandbox (cần mạng): `bash scripts/deploy.sh`. Không tự chạy `git push -f` trực tiếp; `-f` chỉ nằm trong script, đẩy lên nhánh `deploy`.
- Trước khi chạy kiểm `ps aux | grep deploy.sh` — đang có phiên khác deploy thì chờ, không chạy chồng.
- Bị hỏi passphrase SSH (sau khi khởi động lại Mac): dừng, báo thầy chạy `ssh-add --apple-use-keychain ~/.ssh/id_ed25519_github`. Không tự chuyển lại HTTPS, không đòi token.
- Commit theo đường dẫn cụ thể (`git commit -- <path>`), không `git add .`/`commit -a`.
