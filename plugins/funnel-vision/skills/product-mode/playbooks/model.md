### Model

**You own the names. A thing has one name everywhere, or it has none.**

1. List the core objects. For each: what it is in one sentence, its attributes, and the actions a user can take on it.
2. Draw the relationships: 1:1, 1:many, many:many. Many:many is where the hard screens come from.
3. Write the glossary (`python3 scripts/vocab_check.py --template`): one term per object, and the names that must not be used for it. Use the word the interface shows the user.
4. `python3 scripts/vocab_check.py docs/product/glossary.csv <repo>`. Each hit is a rename, or a second concept that deserves its own term.
5. Design the URLs from the object hierarchy: readable, shareable, bookmarkable. State what each deep link opens on mobile.
6. Write the permission table: for each role, view, create, edit, delete, share, per object.
7. Plan schema changes as expand, migrate, contract. State which old clients, including installed app versions, keep working at each step (`references/platforms.md`).
8. Derive event names from the objects and actions: `object_action`. The tracking plan and the schema now share a vocabulary.

**Reply:** the objects and relationships, the glossary and the checker's result, the URL scheme, the permission table, the migration steps and which clients survive each.
