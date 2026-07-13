# Design Variations

Different themes for the CoX Mod Adventure interface.

## v1 - Clean Modern (Default)
- **Style**: Clean utility landing page
- **Font**: Outfit (modern sans-serif)
- **Colors**: Dark slate, blue accent
- **Location**: `/pages/`

## v2 - Comic Book KAPOW! Edition
- **Style**: Classic comic book with bold action text
- **Font**: Bebas Neue, Permanent Marker
- **Colors**: Black background, red/yellow/blue highlights, Ben-Day dots
- **Features**: Comic panels, action text with red outlines, retro grid
- **Location**: `/pages/v2/`

## v3 - Noir Detective Files
- **Style**: Gritty detective case files
- **Font**: Playfair Display (serif), Source Code Pro (mono)
- **Colors**: Dark red/black gradient, typewriter text
- **Features**: Evidence board layout, "case files" theming, noir atmosphere
- **Location**: `/pages/v3/`

## v4 - Japanese Manga
- **Style**: Japanese manga with speed lines
- **Font**: Noto Sans JP, RocknRoll One
- **Colors**: Indigo/dark background, red accents
- **Features**: Japanese labels, speed line background, skewed panels
- **Location**: `/pages/v4/`

## v5 - Graphic Novel GRITTY
- **Style**: Street-level comic panel aesthetic
- **Font**: Oswald, Bebas Neue
- **Colors**: Charcoal with double borders, red highlights
- **Features**: Double-border panels, rough edges, "archive files" theming
- **Location**: `/pages/v5/`

## Adding Your Own Assets

To integrate your own comic/book fonts or styles:
1. Place font files in a new `/pages/assets/fonts/` directory
2. Add custom CSS to the respective variation's `<style>` block
3. Reference your superhero art in the panel backgrounds

Each variation is self-contained with inline styles for easy deployment.