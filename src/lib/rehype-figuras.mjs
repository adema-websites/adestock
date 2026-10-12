// Envuelve las imágenes que están solas en un párrafo en <figure><img><figcaption>alt</figcaption></figure>.
export default function rehypeFiguras() {
  const walk = (node) => {
    if (!node.children) return;
    node.children = node.children.map((hijo) => {
      if (hijo.type === 'element' && hijo.tagName === 'p') {
        const utiles = hijo.children.filter((c) => !(c.type === 'text' && !c.value.trim()));
        if (utiles.length === 1 && utiles[0].type === 'element' && utiles[0].tagName === 'img') {
          const img = utiles[0];
          const alt = String(img.properties?.alt ?? '').trim();
          return {
            type: 'element', tagName: 'figure', properties: {},
            children: [img, ...(alt ? [{ type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: alt }] }] : [])],
          };
        }
      }
      walk(hijo);
      return hijo;
    });
  };
  return (tree) => walk(tree);
}
