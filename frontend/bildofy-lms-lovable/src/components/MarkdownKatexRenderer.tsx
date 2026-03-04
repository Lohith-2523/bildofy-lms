import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

type Props = {
  content: string;
};

const MarkdownKatexRenderer: React.FC<Props> = ({ content }) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkMath]}
      rehypePlugins={[rehypeKatex]}
      components={{
        h1: ({ node, ...props }) => (
          <h1 className="text-2xl font-bold mt-6 mb-4" {...props} />
        ),
        h2: ({ node, ...props }) => (
          <h2 className="text-xl font-semibold mt-5 mb-3" {...props} />
        ),
        p: ({ node, ...props }) => (
          <p className="leading-7 mb-3" {...props} />
        ),
        li: ({ node, ...props }) => (
          <li className="ml-6 list-disc mb-1" {...props} />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
};

export default MarkdownKatexRenderer;
