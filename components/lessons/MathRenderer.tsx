"use client";

import { useEffect, useRef } from "react";
import katex from "katex";
import "katex/dist/katex.min.css";

interface Props {
  html: string;
  className?: string;
}

/**
 * Component to render HTML with embedded LaTeX math formulas
 * Uses KaTeX for math rendering
 */
export default function MathRenderer({ html, className }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Find all math elements and render them
    const mathElements = containerRef.current.querySelectorAll(
      ".math-display, .math-inline"
    );

    mathElements.forEach((el) => {
      const isDisplay = el.classList.contains("math-display");
      const latexText = el.getAttribute("data-latex");

      if (!latexText) return;

      try {
        // Clear content first
        el.textContent = "";

        // Render KaTeX
        katex.render(latexText, el as HTMLElement, {
          displayMode: isDisplay,
          throwOnError: false,
        });
      } catch (err) {
        console.error("KaTeX render error:", err);
        el.textContent = latexText; // Fallback to plain text
      }
    });
  }, [html]);

  return (
    <div
      ref={containerRef}
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}
