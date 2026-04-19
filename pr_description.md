# 🧪 Add test for set_metadata in builder.py

## 🎯 What
Added missing test coverage for the `set_metadata` method in `GalleryBuilder` (`autogenstudio.gallery.builder`).

## 📊 Coverage
The new test (`test_set_metadata` in `tests/gallery/test_builder.py`) covers the following scenarios:
- Verifying default metadata attributes on a newly created `GalleryBuilder`.
- Updating all metadata attributes simultaneously and verifying the changes.
- Verifying the method's ability to be chained (i.e. checking that it returns `self`).
- Verifying partial updates (e.g., updating only `author` while leaving other attributes unchanged).

## ✨ Result
Increased test coverage for the `autogenstudio/gallery/builder.py` module, ensuring that the gallery builder correctly updates and maintains metadata state.
