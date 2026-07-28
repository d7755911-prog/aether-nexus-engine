"use client";

import React, { Suspense, useRef } from "react";
import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import { OrbitControls, Stage, PerspectiveCamera, Html } from "@react-three/drei";
import * as THREE from "three";

// ✅ 1. Props interface properly exported
export interface Viewport3DProps {
  textureUrl: string | null;
  geometryType: "sphere" | "cube" | "plane" | "torus";
  roughness?: number;
  metalness?: number;
}

function TexturedMesh({
  textureUrl,
  geometryType,
  roughness = 0.3,
  metalness = 0.2,
}: Viewport3DProps) {
  const meshRef = useRef<THREE.Mesh>(null!);

  const texture = textureUrl
    ? useLoader(THREE.TextureLoader, textureUrl)
    : null;

  if (texture) {
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    texture.colorSpace = THREE.SRGBColorSpace;
  }

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.2;
    }
  });

  const renderGeometry = () => {
    switch (geometryType) {
      case "sphere":
        return <sphereGeometry args={[1.5, 64, 64]} />;
      case "plane":
        return <planeGeometry args={[3, 3, 32, 32]} />;
      case "torus":
        return <torusGeometry args={[1.2, 0.4, 32, 100]} />;
      case "cube":
      default:
        return <boxGeometry args={[2, 2, 2]} />;
    }
  };

  return (
    <mesh ref={meshRef} castShadow receiveShadow>
      {renderGeometry()}
      <meshStandardMaterial
        map={texture}
        roughness={roughness}
        metalness={metalness}
        color={!texture ? "#1e293b" : "#ffffff"}
      />
    </mesh>
  );
}

// ✅ 2. DEFAULT EXPORT Component
export default function Viewport3D({
  textureUrl,
  geometryType,
  roughness = 0.3,
  metalness = 0.2,
}: Viewport3DProps) {
  return (
    <div className="relative w-full h-full bg-slate-950 rounded-xl overflow-hidden border border-slate-800 shadow-2xl">
      <div className="absolute top-4 left-4 z-10 flex items-center gap-3 bg-slate-900/80 backdrop-blur-md px-4 py-2 rounded-lg border border-slate-700/50">
        <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
        <span className="text-xs font-mono font-semibold text-slate-200 uppercase tracking-wider">
          AETHER-3D Viewport
        </span>
      </div>

      <Canvas shadows gl={{ antialias: true, preserveDrawingBuffer: true }}>
        <PerspectiveCamera makeDefault position={[0, 0, 5]} fov={50} />
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} castShadow />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} color="#38bdf8" />

        <Suspense
          fallback={
            <Html center>
              <div className="flex flex-col items-center gap-2 bg-slate-900/90 px-4 py-3 rounded-lg border border-slate-700">
                <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
                <p className="text-xs font-mono text-cyan-400">Streaming B2 Texture...</p>
              </div>
            </Html>
          }
        >
          <Stage environment="city" intensity={0.5} adjustCamera={false}>
            <TexturedMesh
              textureUrl={textureUrl}
              geometryType={geometryType}
              roughness={roughness}
              metalness={metalness}
            />
          </Stage>
        </Suspense>

        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={false}
          maxPolarAngle={Math.PI / 1.5}
          minDistance={2}
          maxDistance={10}
        />
      </Canvas>
    </div>
  );
}