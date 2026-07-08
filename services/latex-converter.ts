/**
 * LaTeX → HTML Converter
 * Converts LaTeX document structure + math formulas to HTML
 */

interface ConversionResult {
  html: string;
  latex: string; // Lưu LaTeX gốc
  mathCount: number;
}

/**
 * Convert LaTeX document to HTML
 * Handles:
 * - \section{...}, \subsection{...}, \subsubsection{...}
 * - \paragraph{...}
 * - Inline math: $...$, \(...\)
 * - Display math: $$...$$ \[...\]
 * - Environments: \begin{itemize}...\end{itemize}, etc.
 */
export function latexToHtml(latexText: string): ConversionResult {
  let html = latexText;
  let mathCount = 0;

  // Step 1: Escape HTML special chars (but preserve LaTeX commands)
  html = html
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Step 2: Convert LaTeX structure to HTML
  // \section{...} → <h1>...</h1>
  html = html.replace(/\\section\{([^}]+)\}/g, "<h1>$1</h1>");
  html = html.replace(/\\subsection\{([^}]+)\}/g, "<h2>$1</h2>");
  html = html.replace(/\\subsubsection\{([^}]+)\}/g, "<h3>$1</h3>");
  html = html.replace(/\\paragraph\{([^}]+)\}/g, "<h4>$1</h4>");

  // Step 3: Convert itemize → <ul>
  // \begin{itemize} ... \item text \end{itemize}
  html = html.replace(/\\begin\{itemize\}/g, "<ul>");
  html = html.replace(/\\end\{itemize\}/g, "</ul>");
  html = html.replace(/\\item\s+/g, "<li>");
  html = html.replace(/\n(<\/li>)?(?=\n|\\item|<\/ul>)/g, "</li>");

  // Step 4: Convert enumerate → <ol>
  html = html.replace(/\\begin\{enumerate\}/g, "<ol>");
  html = html.replace(/\\end\{enumerate\}/g, "</ol>");

  // Step 5: Convert common LaTeX commands
  html = html.replace(/\\textbf\{([^}]+)\}/g, "<strong>$1</strong>");
  html = html.replace(/\\textit\{([^}]+)\}/g, "<em>$1</em>");
  html = html.replace(/\\emph\{([^}]+)\}/g, "<em>$1</em>");
  html = html.replace(/\\texttt\{([^}]+)\}/g, "<code>$1</code>");
  html = html.replace(/\\textcolor\{[^}]+\}\{([^}]+)\}/g, "$1"); // Simplified
  html = html.replace(/\\\\/g, "<br />");

  // Step 6: Mark math zones for later rendering
  // Display math: $$...$$ → <div class="math-display">...</div>
  html = html.replace(/\$\$([\s\S]*?)\$\$/g, (match, math) => {
    mathCount++;
    return `<div class="math-display" data-latex="${escapeHtml(math)}">$$${math}$$</div>`;
  });

  // Display math: \[...\]
  html = html.replace(/\\\[([\s\S]*?)\\\]/g, (match, math) => {
    mathCount++;
    return `<div class="math-display" data-latex="${escapeHtml(math)}">\\[${math}\\]</div>`;
  });

  // Inline math: $...$ → <span class="math-inline">...</span>
  html = html.replace(/\$([^\$\n]+?)\$/g, (match, math) => {
    mathCount++;
    return `<span class="math-inline" data-latex="${escapeHtml(math)}">$${math}$</span>`;
  });

  // Inline math: \(...\)
  html = html.replace(/\\\(([^\)]+?)\\\)/g, (match, math) => {
    mathCount++;
    return `<span class="math-inline" data-latex="${escapeHtml(math)}">\\(${math}\\)</span>`;
  });

  // Step 7: Convert double newlines to paragraphs
  html = html.replace(/\n\n+/g, "</p><p>");
  html = "<p>" + html + "</p>";

  // Step 8: Clean up empty paragraphs
  html = html.replace(/<p>\s*<\/p>/g, "");
  html = html.replace(/<p>(<[hu][1-4]|<[ou]l|<ol)/g, "$1");
  html = html.replace(/(<\/[hu][1-4]>|<\/[ou]l>|<\/ol>)<\/p>/g, "$1");

  // Step 9: Add styling classes for better formatting
  html = html.replace(/<h1>/g, '<h1 class="text-2xl font-bold mt-4 mb-2">');
  html = html.replace(/<h2>/g, '<h2 class="text-xl font-bold mt-3 mb-1.5">');
  html = html.replace(/<h3>/g, '<h3 class="text-lg font-semibold mt-2 mb-1">');
  html = html.replace(/<h4>/g, '<h4 class="font-semibold mt-2 mb-1">');
  html = html.replace(/<p>/g, '<p class="text-base leading-relaxed my-2">');
  html = html.replace(/<ul>/g, '<ul class="list-disc list-inside my-2 ml-4">');
  html = html.replace(/<ol>/g, '<ol class="list-decimal list-inside my-2 ml-4">');
  html = html.replace(/<li>/g, '<li class="my-1">');
  html = html.replace(/<strong>/g, '<strong class="font-bold">');
  html = html.replace(/<em>/g, '<em class="italic">');
  html = html.replace(/<code>/g, '<code class="bg-slate-200 text-slate-900 px-1 rounded font-mono text-sm">');

  return {
    html,
    latex: latexText,
    mathCount,
  };
}

/**
 * Render math formulas in HTML
 * Should be called client-side using KaTeX
 */
export function renderMathInHtml(html: string): string {
  // This function should be called in browser with KaTeX
  // It will find .math-display and .math-inline elements
  // and render them using KaTeX.render()
  return html;
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/**
 * Validate LaTeX syntax (basic check)
 */
export function validateLatexSyntax(latex: string): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Check for unmatched braces
  let braceCount = 0;
  for (const char of latex) {
    if (char === "{") braceCount++;
    if (char === "}") braceCount--;
    if (braceCount < 0) {
      errors.push("Dấu } không khớp với {");
      break;
    }
  }
  if (braceCount > 0) {
    errors.push("Thiếu dấu }");
  }

  // Check for unmatched $
  const mathCount = (latex.match(/\$/g) || []).length;
  if (mathCount % 2 !== 0) {
    errors.push("Thiếu dấu $ để đóng công thức");
  }

  // Check for unmatched \begin and \end
  const beginCount = (latex.match(/\\begin\{/g) || []).length;
  const endCount = (latex.match(/\\end\{/g) || []).length;
  if (beginCount !== endCount) {
    errors.push("Thiếu \\end để đóng \\begin");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
