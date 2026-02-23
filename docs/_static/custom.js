/**
 * Fix for mermaid diagram SVG height issue.
 * 
 * The mermaid extension generates inline <style> with fixed height (500px)
 * which causes large gaps above and below diagrams.
 * 
 * CSS cannot override this because the inline style loads after custom.css.
 * MutationObserver watches for DOM changes and fixes the height dynamically.
 */
const observer = new MutationObserver(function(mutations) {
    const svgs = document.querySelectorAll('.mermaid-container > pre > svg');
    svgs.forEach(function(svg) {
        svg.style.height = 'auto';
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});