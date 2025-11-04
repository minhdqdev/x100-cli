# Getting Started with x100 Workflow Automation

Cài đặt và sử dụng x100 với Claude Code trong 5 phút.

## Cài Đặt Nhanh

### 1. Clone và Setup

```bash
# Clone x100 vào project
git clone https://github.com/minhdqdev/x100-template.git .x100
chmod +x .x100/x100
ln -s .x100/x100 x100

# Initialize project
./x100 init
```

### 2. Setup Claude Code

```bash
# Interactive setup
./x100
# → Select "Setup AI Agent" → "Claude Code"

# Enable workflow automation
./x100 workflow-enable
```

### 3. Xong! Dùng Thử

Trong Claude Code:

```
/workflow docs/user-stories/US-001-feature.md
```

Hoặc từng bước:

```
/start US-001 → /code → /test → /review → /done
```

## Các Commands Có Sẵn

| Command | Mô Tả |
|---------|-------|
| `/start` | Bắt đầu feature, tạo spec |
| `/spec` | Tạo technical specification |
| `/code` | Implement code từ spec |
| `/test` | Tạo và chạy tests |
| `/review` | Code review toàn diện |
| `/done` | Commit feature |
| `/workflow` | **Full automation** tất cả bước trên |

## Workflow Tự Động

```
User Story → Spec → Code → Test → Review → Done
```

### Full Automation
```bash
/workflow US-001
```

### Step-by-Step
```bash
/start US-001
/code
/test
/review
/done
```

## Quản Lý Commands & Agents

```bash
# List tất cả
./x100 command list
./x100 agent list

# Enable/disable
./x100 command enable start
./x100 agent enable spec-writer

# Interactive menu
./x100
```

## Docs Đầy Đủ

- **Setup chi tiết**: [SETUP.md](./SETUP.md)
- **Workflow guide**: [resources/WORKFLOW.md](./resources/WORKFLOW.md)
- **Quick start**: [resources/WORKFLOW_QUICKSTART.md](./resources/WORKFLOW_QUICKSTART.md)

> **Note:** Paths above are for viewing the repo directly. When integrated as `.x100/` in your project, paths will be `.x100/resources/...`

## Ví Dụ Workflow

### Ví dụ 1: Test với Example Feature (Recommended)

Try the included example first:

```bash
# Trong Claude Code
/workflow docs/user-stories/US-001-example-feature.md

# Tự động:
# 1. Tạo spec: SPEC-001-example-feature.md
# 2. Implement calculator code
# 3. Tạo unit tests với 80%+ coverage
# 4. Review quality & security
# 5. Commit với message rõ ràng

# Expected time: 5-10 minutes
```

### Ví dụ 2: Your Own Feature

```bash
# Create your user story in docs/user-stories/
# Then run workflow
/workflow docs/user-stories/US-002-your-feature.md
```

### Ví dụ 3: Bug Fix

```bash
/code "Fix authentication timeout bug"
/test
/review
/done "fix: resolve auth timeout issue"
```

### Ví dụ 4: Quick Review

```bash
# Sau khi code manually
/review
/test
/done
```

## Troubleshooting

**"uv not found"**
```bash
brew install uv
```

**Commands không hiện trong Claude Code**
```bash
./x100 workflow-enable
# Restart Claude Code
```

**Permission denied**
```bash
chmod +x .x100/x100
```

## So Sánh với BMAD/SpecKit

| Feature | x100 | BMAD | SpecKit |
|---------|:----:|:----:|:-------:|
| Workflow automation | ✅ | ✅ | ⚠️ |
| CLI management | ✅ | ❌ | ❌ |
| Easy setup | ✅ | ⚠️ | ⚠️ |
| Low overhead | ✅ | ❌ | ❌ |

## Next Steps

1. ✅ Setup xong → Đọc [WORKFLOW_QUICKSTART.md](./.x100/resources/WORKFLOW_QUICKSTART.md)
2. ✅ Tạo user story đầu tiên
3. ✅ Chạy `/workflow` trong Claude Code
4. ✅ Customize theo nhu cầu

---

**Sẵn sàng?**

```bash
./x100 workflow-enable
```

Rồi trong Claude Code:
```
/workflow your-first-feature.md
```
