import React from 'react';
import { Composition } from 'remotion';
import { Test } from './Test';
export const Root: React.FC = () => (
  <Composition id="Test" component={Test} durationInFrames={90} fps={30} width={1920} height={1080} />
);
