import React from 'react';
import { Composition } from 'remotion';
import { Test } from './Test';
import { Sheet } from './Sheet';
import { DocFull, FULL_FRAMES } from './Doc';
export const Root: React.FC = () => (
  <>
    <Composition id="Test" component={Test} durationInFrames={90} fps={30} width={1920} height={1080} />
    <Composition id="Sheet" component={Sheet} durationInFrames={30} fps={30} width={1920} height={1080} />
    <Composition id="Full" component={DocFull} durationInFrames={FULL_FRAMES} fps={30} width={1920} height={1080} />
  </>
);
