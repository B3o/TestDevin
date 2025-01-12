import React, { Suspense } from 'react';
import * as THREE from 'three';
import { Canvas } from '@react-three/fiber';
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';

function Ground() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
      <planeGeometry args={[100, 100, 50, 50]} />
      <meshPhongMaterial
        color={0x000913}
        emissive={0x00ffff}
        emissiveIntensity={0.2}
      />
    </mesh>
  );
}

function MaglevTrack() {
  const [progress, setProgress] = React.useState(0);
  
  React.useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => (prev + 0.001) % 1);
    }, 16);
    return () => clearInterval(interval);
  }, []);

  const trackPoints = [
    new THREE.Vector3(-15, 8, -15),
    new THREE.Vector3(-15, 8, 15),
    new THREE.Vector3(15, 8, 15),
    new THREE.Vector3(15, 8, -15),
    new THREE.Vector3(-15, 8, -15)
  ];
  
  const trackCurve = new THREE.CatmullRomCurve3(trackPoints);
  const position = trackCurve.getPointAt(progress);
  const tangent = trackCurve.getTangentAt(progress);
  
  return (
    <>
      <mesh>
        <tubeGeometry args={[trackCurve, 200, 0.2, 8, true]} />
        <meshPhongMaterial
          color={0x101010}
          emissive={0x39ff14}
          emissiveIntensity={1.0}
          shininess={100}
        />
      </mesh>
      <mesh position={position} quaternion={new THREE.Quaternion().setFromUnitVectors(
        new THREE.Vector3(0, 0, 1),
        tangent
      )}>
        <capsuleGeometry args={[0.3, 2, 4, 8]} />
        <meshPhongMaterial
          color={0x202020}
          emissive={0x39ff14}
          emissiveIntensity={0.5}
          shininess={100}
        />
      </mesh>
    </>
  );
}

function Drones() {
  const [time, setTime] = React.useState(0);
  
  React.useEffect(() => {
    const interval = setInterval(() => {
      setTime(t => t + 0.016);
    }, 16);
    return () => clearInterval(interval);
  }, []);

  const drones = Array.from({ length: 5 }, (_, i) => {
    const baseX = Math.random() * 30 - 15;
    const baseY = Math.random() * 5 + 10;
    const baseZ = Math.random() * 30 - 15;
    const offset = i * Math.PI * 0.4;
    
    const x = baseX + Math.sin(time + offset) * 2;
    const y = baseY + Math.sin(time * 2 + offset) * 0.5;
    const z = baseZ + Math.cos(time + offset) * 2;
    
    return (
      <group key={i} position={[x, y, z]} rotation={[0, time + offset, 0]}>
        <mesh>
          <boxGeometry args={[0.5, 0.2, 0.5]} />
          <meshPhongMaterial
            color={0x202020}
            emissive={0xff1493}
            emissiveIntensity={0.5}
          />
        </mesh>
        <mesh position={[0, -1, 0]}>
          <cylinderGeometry args={[0.1, 0.3, 2, 8]} />
          <meshPhongMaterial
            color={0xffffff}
            transparent
            opacity={0.2}
            emissive={0xffffff}
            emissiveIntensity={1.0}
          />
        </mesh>
      </group>
    );
  });
  
  return <>{drones}</>;
}

function NeonPipes() {
  const pipes = Array.from({ length: 15 }, (_, i) => {
    const points = Array.from({ length: 4 }, () => [
      Math.random() * 20 - 10,
      Math.random() * 10 + 5,
      Math.random() * 20 - 10
    ]);
    
    const curve = new THREE.CatmullRomCurve3(
      points.map(([x, y, z]) => new THREE.Vector3(x, y, z))
    );
    
    return (
      <mesh key={i}>
        <tubeGeometry args={[curve, 100, 0.1, 8, false]} />
        <meshPhongMaterial
          color={0x000000}
          emissive={Math.random() > 0.5 ? 0xff1493 : 0x00ffff}
          emissiveIntensity={2.0}
          shininess={100}
        />
      </mesh>
    );
  });

  return <>{pipes}</>;
}

function CyberpunkScene() {
  return (
    <>
      <PerspectiveCamera makeDefault position={[8, 5, 8]} />
      <OrbitControls enablePan={false} maxDistance={20} minDistance={5} />
      
      <color attach="background" args={[0x000913]} />
      <fog attach="fog" args={[0x000913, 0, 50]} />
      
      <ambientLight intensity={0.1} />
      <hemisphereLight args={[0x000913, 0xff1493, 0.3]} />
      
      <pointLight position={[5, 5, 5]} color={0xff1493} intensity={1} distance={20} />
      <pointLight position={[-5, 5, -5]} color={0x00ffff} intensity={1} distance={20} />
      <pointLight position={[0, 10, 0]} color={0xff00ff} intensity={0.5} distance={20} />
      
      <Buildings />
      <Ground />
      <NeonPipes />
      <MaglevTrack />
      <Drones />
      <EffectComposer>
        <Bloom
          intensity={2.0}
          radius={0.5}
          mipmapBlur
          luminanceThreshold={0.2}
        />
      </EffectComposer>
    </>
  );
}

function Buildings() {
  const buildingGeometries = [
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.CylinderGeometry(0.5, 0.5, 1, 8),
    new THREE.BoxGeometry(0.8, 1, 0.8)
  ];

  const buildings = Array.from({ length: 100 }, (_, i) => {
    const height = Math.random() * 6 + 2;
    const width = Math.random() * 0.8 + 0.5;
    const depth = Math.random() * 0.8 + 0.5;
    const x = Math.random() * 20 - 10;
    const z = Math.random() * 20 - 10;
    const color = Math.random() > 0.5 ? 0xff1493 : 0x00ffff;
    
    return (
      <group key={i} position={[x, height / 2, z]} rotation={[0, Math.random() * Math.PI * 2, 0]}>
        <mesh
          geometry={buildingGeometries[Math.floor(Math.random() * buildingGeometries.length)]}
          scale={[width, height, depth]}
        >
          <meshPhongMaterial
            color={0x0a0a0a}
            emissive={color}
            emissiveIntensity={2.0}
            specular={0x111111}
            shininess={30}
            flatShading
          />
        </mesh>
        {Math.random() > 0.7 && (
          <>
            <Billboard position={[width / 2 + 0.1, 0, 0]} />
            <Billboard position={[-width / 2 - 0.1, 0, 0]} rotation={[0, Math.PI, 0]} />
          </>
        )}
      </group>
    );
  });

  return <>{buildings}</>;
}

interface BillboardProps {
  position?: [number, number, number];
  rotation?: [number, number, number];
}

function Billboard({ position = [0, 0, 0], rotation = [0, 0, 0] }: BillboardProps) {
  return (
    <mesh position={position} rotation={rotation}>
      <planeGeometry args={[2, 3]} />
      <meshPhongMaterial
        color={0x00ffff}
        emissive={0x00ffff}
        emissiveIntensity={1}
        transparent
        opacity={0.5}
      />
    </mesh>
  );
}

export function PixelWorld() {
  return (
    <div className="w-full h-[600px] bg-black">
      <Canvas
        dpr={[1, 2]}
        camera={{ position: [8, 5, 8], fov: 75 }}
        gl={{
          antialias: false,
          powerPreference: "high-performance",
          alpha: true
        }}
      >
        <Suspense fallback={null}>
          <CyberpunkScene />
        </Suspense>
      </Canvas>
    </div>
  );
}
