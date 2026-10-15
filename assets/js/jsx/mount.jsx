import React, { Component, useEffect } from 'react';
import { createRoot } from 'react-dom/client';

class Boundary extends Component {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  componentDidCatch(error) { this.props.fail(error); }
  render() { return this.state.failed ? null : this.props.children; }
}
function Ready({ children, ready }) {
  useEffect(() => { ready(); }, [ready]);
  return children;
}
export function mount(container, Widget, { ready, fail, prefix }) {
  if (!Widget) throw new Error('JSX module must have a default component export');
  const root = createRoot(container, { identifierPrefix: prefix, onUncaughtError: fail });
  root.render(<Boundary fail={fail}><Ready ready={ready}><Widget /></Ready></Boundary>);
  return root;
}
