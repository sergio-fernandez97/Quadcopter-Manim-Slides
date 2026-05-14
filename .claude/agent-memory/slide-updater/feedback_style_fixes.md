---
name: style-fixes-on-update
description: When updating any slide, also fix old-style animation patterns in the same file
metadata:
  type: feedback
---

When any slide update task is performed, always fix these old-style patterns found in the same file:

- `self.add(title)` → `self.play(FadeIn(title))`
- `title.to_edge(UP)` → `title.to_edge(UP, buff=0.5)`
- `Write(mobject)` → `FadeIn(mobject)` (Write() is banned per style guide)
- `self.wait(2)` before `self.next_slide()` → `self.wait(0.5)` before `self.next_slide()`
- `self.wait(1)` before `self.next_slide()` → `self.wait(0.5)` before `self.next_slide()`

**Why:** The style guide in CLAUDE.md prohibits Write() and requires wait(0.5) before next_slide(). These fixes are included in the ADDITIONAL_INSTRUCTIONS of update tasks for this project.

**How to apply:** Scan the full file when reading it in Step 1. Apply all style fixes as part of the same write operation as the content additions.
