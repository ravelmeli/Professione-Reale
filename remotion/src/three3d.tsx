import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import * as THREE from 'three';
import { useThree } from '@react-three/fiber';

const M = (c: string) => <meshBasicMaterial color={c} />;
const Box: React.FC<{ p: [number, number, number]; s: [number, number, number]; c: string; ol?: boolean }> = ({ p, s, c, ol = true }) => (
  <group position={p}>
    <mesh><boxGeometry args={s} />{M(c)}</mesh>
    {ol && <mesh scale={[1.035, 1.035, 1.035]}><boxGeometry args={s} /><meshBasicMaterial color="#111" side={THREE.BackSide} /></mesh>}
  </group>
);
const Wheel: React.FC<{ p: [number, number, number] }> = ({ p }) => (
  <group position={p} rotation={[0, 0, Math.PI / 2]}><mesh><cylinderGeometry args={[0.55, 0.55, 0.5, 20]} />{M('#1d1f27')}</mesh><mesh scale={[1.06, 1.02, 1.06]}><cylinderGeometry args={[0.55, 0.55, 0.5, 20]} /><meshBasicMaterial color="#111" side={THREE.BackSide} /></mesh><mesh position={[0, 0.26, 0]}><cylinderGeometry args={[0.24, 0.24, 0.02, 14]} />{M('#c9ced6')}</mesh></group>
);
export const Truck3D: React.FC<{ x?: number; z?: number; ry?: number }> = ({ x = 0, z = 0, ry = 0 }) => (
  <group position={[x, 0, z]} rotation={[0, ry, 0]}>
    <Box p={[0, 1.9, -1.2]} s={[2.4, 2.6, 7]} c="#d9d4c4" /><Box p={[0, 3.12, -1.2]} s={[2.42, 0.34, 7.02]} c="#8FD23F" />
    <Box p={[0, 1.3, 3.1]} s={[2.3, 1.9, 2]} c="#c33631" /><Box p={[0, 1.95, 4.15]} s={[1.9, 0.9, 0.06]} c="#9fd0ff" ol={false} />
    <Box p={[0, 0.55, 0.6]} s={[2.2, 0.3, 9]} c="#2a2f3c" />
    {[-1.2, 1.2].map((sx) => [-3.6, -2.4, 0.2, 3.4].map((wz, i) => <Wheel key={`${sx}${i}`} p={[sx, 0.55, wz]} />))}
    <mesh position={[0.7, 0.9, 4.2]}><sphereGeometry args={[0.16, 10, 10]} />{M('#fff6c0')}</mesh><mesh position={[-0.7, 0.9, 4.2]}><sphereGeometry args={[0.16, 10, 10]} />{M('#fff6c0')}</mesh>
  </group>
);
const Flag: React.FC<{ x: number; z: number; cols: string[]; v?: boolean; t: number }> = ({ x, z, cols, v, t }) => (
  <group position={[x, 0, z]}>
    <mesh position={[0, 3, 0]}><cylinderGeometry args={[0.06, 0.06, 6, 8]} />{M('#8a93a6')}</mesh>
    {cols.map((c, i) => <mesh key={i} position={[0.9 + (v ? 0.55 * (i - 1) : 0), v ? 5.3 : 5.5 - 0.5 * i, 0]} rotation={[0, Math.sin(t * 3 + i) * 0.12, 0]}><planeGeometry args={v ? [0.55, 1.5] : [1.6, 0.5]} /><meshBasicMaterial color={c} side={THREE.DoubleSide} /></mesh>)}
  </group>
);
const Road: React.FC<{ t: number; night?: boolean }> = ({ t, night }) => (
  <group>
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}><planeGeometry args={[200, 400]} />{M(night ? '#1d2a2a' : '#5b8a58')}</mesh>
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}><planeGeometry args={[9, 400]} />{M(night ? '#232a3c' : '#3a3f4d')}</mesh>
    {[-4.4, 4.4].map((x) => <mesh key={x} rotation={[-Math.PI / 2, 0, 0]} position={[x, 0.02, 0]}><planeGeometry args={[0.18, 400]} />{M('#f4f1ea')}</mesh>)}
    {Array.from({ length: 40 }).map((_, i) => <mesh key={i} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, ((i * 6 + (t * 14) % 6) - 120)]}><planeGeometry args={[0.2, 2.6]} />{M(night ? '#ffe08a' : '#e0a32e')}</mesh>)}
  </group>
);
export const Showpiece: React.FC<{ kind: 'border' | 'fleet'; p: number; t: number }> = ({ kind, p, t }) => {
  const { width, height } = useVideoConfig();
  const sky = kind === 'border' ? '#9ec7ee' : '#0d1226';
  if (kind === 'border') {
    const tz = -20 + p * 30;
    const cam = [-11 + p * 15, 4.6 - p * 1.2, tz - 24 + p * 7] as [number, number, number];
    return (
      <ThreeCanvas width={width} height={height} camera={{ position: cam, fov: 48, near: 0.1, far: 500 }} onCreated={({ camera }) => camera.lookAt(0, 2.4, tz + 5)}>
        <color attach="background" args={[sky]} /><fog attach="fog" args={[sky, 40, 190]} />
        <CamLook pos={cam} look={[0, 2.2, tz + 9]} />
        <Road t={t} />
        <Truck3D z={tz} />
        <Flag x={-6} z={22} cols={['#2a5cd0', '#fff', '#e5392b']} v t={t} /><Flag x={6} z={30} cols={['#17141f', '#e5392b', '#ffd23f']} t={t} /><Flag x={-6} z={38} cols={['#e5392b', '#ffd23f', '#e5392b']} t={t} /><Flag x={6} z={46} cols={['#e5392b', '#fff', '#e5392b']} t={t} />
        <Box p={[0, 5.5, 55]} s={[16, 0.6, 0.6]} c="#2C3E50" /><Box p={[-8, 2.7, 55]} s={[0.6, 5.4, 0.6]} c="#2C3E50" /><Box p={[8, 2.7, 55]} s={[0.6, 5.4, 0.6]} c="#2C3E50" />
        {[-70, -40, 60, 90].map((z, i) => <mesh key={i} position={[(i % 2 ? 1 : -1) * 20, 6, z]}><coneGeometry args={[10, 12, 6]} />{M('#7aa48f')}</mesh>)}
      </ThreeCanvas>
    );
  }
  const a = 0.5 + p * 1.4; const r = 24;
  const cam = [Math.cos(a) * r, 4.2 - p * 1.2, Math.sin(a) * r] as [number, number, number];
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: cam, fov: 46, near: 0.1, far: 300 }}>
      <color attach="background" args={[sky]} /><fog attach="fog" args={[sky, 30, 120]} />
      <CamLook pos={cam} look={[0, 2.2, 0]} />
      <mesh rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[300, 300]} />{M('#1c2238')}</mesh>
      {Array.from({ length: 120 }).map((_, i) => <mesh key={i} position={[((i * 37) % 160) - 80, 30 + (i % 7) * 6, ((i * 53) % 160) - 80]}><sphereGeometry args={[0.12, 5, 5]} />{M('#cfd8f0')}</mesh>)}
      {[[-10, -2, 0.12], [-3.4, -4, 0], [3.4, -4, 0], [10, -2, -0.12], [0, 9, 0.5]].map(([x, z, ry], i) => <Truck3D key={i} x={x} z={z} ry={ry} />)}
      <mesh position={[-14, 5, 0]}><cylinderGeometry args={[0.15, 0.15, 10, 8]} />{M('#2a3350')}</mesh><mesh position={[-14, 10.2, 0]}><sphereGeometry args={[0.9, 10, 10]} />{M('#fff0aa')}</mesh>
      <Box p={[0, 3, -24]} s={[26, 6, 3]} c="#2a3350" /><Box p={[0, 2.2, -22.4]} s={[7, 4.4, 0.1]} c="#f0d58a" ol={false} />
    </ThreeCanvas>
  );
};
const CamLook: React.FC<{ pos: [number, number, number]; look: [number, number, number] }> = ({ pos, look }) => {
  const { camera } = useThree();
  camera.position.set(...pos); camera.lookAt(...look); camera.updateProjectionMatrix();
  return null;
};
