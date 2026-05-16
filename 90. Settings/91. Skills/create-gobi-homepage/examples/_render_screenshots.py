"""Render JPG screenshots of each template with a stubbed window.gobi.

Run:
    python _render_screenshots.py

Output: <style>.jpg in the same directory.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
TEMPLATES_DIR = HERE.parent / "templates"
STYLES = ["neon-terminal", "minimal-editorial", "magazine", "brutalist"]

VIEWPORT = {"width": 1440, "height": 1024}

# JS injected before any page script runs. Stubs window.gobi with fixture data
# so templates render fully (hero, KGraph, BU grid) without a live Gobi backend.
GOBI_STUB = r"""
window.gobi = {
    vault: {
        vaultId: "demo-vault-001",
        title: "jyk — Demo Brain",
        description: "Curating notes, code, and conversations across PKM, AI, and music.",
        thumbnailPath: null,
        tags: ["pkm", "ai", "design"],
        ownerName: "Jin",
        ownerProfilePictureUrl: null,
        webdriveUrl: "https://example.com",
        slug: "jyk"
    },
    _posts: [
        { id: 1,  title: "Building a Skill Library on Top of Claude Code",
          content: "Skills compose. The shape of the skill matters more than the prompt. Here is what I learned in three months.",
          topics: [{name:"AI4PKM"},{name:"Claude Code"},{name:"Skills"}],
          createdAt: "2026-05-12T10:00:00Z" },
        { id: 2,  title: "A Quieter Brain Page",
          content: "Editorial typography over neon. When the page is read every day, calm beats spectacle.",
          topics: [{name:"Design"},{name:"Frontend"},{name:"PKM"}],
          createdAt: "2026-05-10T08:00:00Z" },
        { id: 3,  title: "Voice Mode is Underrated",
          content: "Speaking to a model on a walk closes a gap I did not know existed. Capture beats curation.",
          topics: [{name:"Voice"},{name:"AI4PKM"},{name:"PKM"}],
          createdAt: "2026-05-08T16:00:00Z" },
        { id: 4,  title: "Topics, Not Tags",
          content: "Tags are a flat namespace. Topics are clusters. The Knowledge Graph rewards the difference.",
          topics: [{name:"PKM"},{name:"Knowledge Graph"},{name:"Design"}],
          createdAt: "2026-05-06T12:00:00Z" },
        { id: 5,  title: "Frontend as a Read-First Surface",
          content: "Most of the time the homepage is read, not edited. Optimize for the silent visit.",
          topics: [{name:"Frontend"},{name:"Design"},{name:"UX"}],
          createdAt: "2026-05-04T09:00:00Z" },
        { id: 6,  title: "On Compound Skills",
          content: "A small skill that calls another skill is more powerful than a giant prompt. Composition wins.",
          topics: [{name:"AI4PKM"},{name:"Skills"},{name:"Claude Code"}],
          createdAt: "2026-05-02T14:00:00Z" },
        { id: 7,  title: "Eastern Washington in Late Spring",
          content: "The Palouse, Steptoe Butte, and the Snake River canyon. Six days, two passengers, one mission.",
          topics: [{name:"Travel"},{name:"PNW"},{name:"Family"}],
          createdAt: "2026-04-29T18:00:00Z" },
        { id: 8,  title: "Why I Keep Coming Back to Helvetica",
          content: "Boring tools age well. Helvetica is the linen of typography. It does not pretend, and it does not break.",
          topics: [{name:"Design"},{name:"Typography"},{name:"UX"}],
          createdAt: "2026-04-27T11:00:00Z" }
    ],
    listPersonalPosts: async function({limit=8, cursor=null}={}){
        const start = cursor ? parseInt(cursor, 10) : 0;
        const slice = this._posts.slice(start, start+limit);
        const next = (start+limit) < this._posts.length ? String(start+limit) : null;
        return { data: slice, pagination: { nextCursor: next, hasMore: !!next } };
    },
    listBrainUpdates: function(opts){ return this.listPersonalPosts(opts); },
    getSessions: async function(){ return { data: [{ sessionId: "demo-session", messageCount: 0, lastMessageAt: null }] }; },
    loadMessages: async function(){ return { messages: [] }; },
    sendMessage: async function(){ /* no-op in demo */ },
    readFile: async function(){ throw new Error("readFile not available in demo"); },
    listFiles: async function(){ return []; },
    fileExists: async function(){ return false; }
};
"""


def render(style: str, p):
    template_path = TEMPLATES_DIR / f"{style}.html"
    output_path = HERE / f"{style}.jpg"
    if not template_path.exists():
        print(f"!! missing: {template_path}")
        return
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport=VIEWPORT, device_scale_factor=2)
    ctx.add_init_script(GOBI_STUB)
    page = ctx.new_page()
    page.goto(template_path.as_uri(), wait_until="networkidle")
    # let the D3 simulation settle and fonts load
    page.wait_for_timeout(2500)
    page.screenshot(path=str(output_path), type="jpeg", quality=85, full_page=True)
    browser.close()
    size_kb = output_path.stat().st_size / 1024
    print(f"   {style}.jpg  ({size_kb:.0f} KB)")


def main():
    print("Rendering template screenshots...")
    with sync_playwright() as p:
        for style in STYLES:
            render(style, p)
    print("Done.")


if __name__ == "__main__":
    main()
