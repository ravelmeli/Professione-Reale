import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate } from 'remotion';
import { ThreeCanvas } from '@remotion/three';

const Flat: React.FC = () => {
  const f = useCurrentFrame();
  const z = 1 + 0.001 * f;
  return (
    <AbsoluteFill style={{ background: '#13192B' }}>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ transform: `scale(${z})` }}>
        <rect x={0} y={690} width={1920} height={390} fill="#1c2238" />
        <circle cx={500} cy={500} r={60} fill="#f0b789" stroke="#111" strokeWidth={4.5} />
        <text x={900} y={400} fill="#F4F1EA" fontSize={80}>Remotion SVG ok</text>
      </svg>
    </AbsoluteFill>
  );
};
const Box: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <mesh rotation={[0.4, f * 0.05, 0]}>
      <boxGeometry args={[2, 1, 4]} />
      <meshBasicMaterial color="#8FD23F" />
    </mesh>
  );
};
export const Test: React.FC = () => (
  <AbsoluteFill>
    <Sequence from={0} durationInFrames={45}><Flat /></Sequence>
    <Sequence from={45} durationInFrames={45}>
      <ThreeCanvas width={1920} height={1080} camera={{ position: [0, 0, 8], fov: 40 }} style={{ background: '#2C3E50' }}>
        <Box />
      </ThreeCanvas>
    </Sequence>
  </AbsoluteFill>
);
