# Fixes

Tool and environment problems that no other skill owns. Search by symptom text. Entry format: `- **<symptom>**: <cause>. <fix>. Check: <how>.` Move an entry into a skill once one owns its area.

## Skills

- **Installed skill differs from the source repository**: installed folders were copies, so edits made in one place drifted. Install each skill as a link to its repository folder (README Installation). Check: `diff -rq <installed>/<skill> <repo>/<skill>` prints nothing.
