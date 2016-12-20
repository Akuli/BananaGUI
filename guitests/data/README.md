# How to create banana.png from banana.odg

1. Modify `banana.odg` in LibreOffice Draw. When you're done, select
    all, right-click and convert to bitmap.
2. LibreOffice doesn't like transparent bitmaps for some reason, so
    save the bitmap as a png file somewhere.
3. Open the temporary png file in GIMP and edit it like this:
    - Add an alpha channel to support transparency.
    - Select everything white.
    - Use the rubber to make everything white transparent and use a
        brush to add some white to the bottom.
4. Export to `banana.png` using GIMP's default settings.
