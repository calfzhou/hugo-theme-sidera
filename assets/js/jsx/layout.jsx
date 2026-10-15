// Optional layout conveniences. Native elements/classes remain first-class;
// these divs add no roles, field behavior or second styling system.
const gaps = { none: 'jsx-gap-none', small: 'jsx-gap-small', normal: '', large: 'jsx-gap-large' };
function layoutClass(base, gap, className) {
  if (!Object.hasOwn(gaps, gap)) throw new Error('Sidera layout: gap must be none, small, normal or large');
  return [base, gaps[gap], className].filter(Boolean).join(' ');
}
export function Stack({ gap = 'normal', className, ...props }) {
  return <div {...props} className={layoutClass('jsx-stack', gap, className)} />;
}
export function Row({ gap = 'normal', className, ...props }) {
  return <div {...props} className={layoutClass('jsx-row', gap, className)} />;
}
