import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Torus, Float, Box } from '@react-three/drei';
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import * as THREE from 'three';

// --- LOGO "IF" GEOMÉTRICO (Minimalista e Neon) ---
function GeometricLogo() {
    // Material Neon Cyan
    const neonMaterial = (
        <meshStandardMaterial 
            color="#22d3ee"       // Cor Base (Ciano)
            emissive="#22d3ee"    // Cor da Luz Própria
            emissiveIntensity={2} // Força do Brilho
            toneMapped={false}
        />
    );

    return (
        <group position={[-0.2, 0, 0]}> {/* Centraliza visualmente */}
            
            {/* LETRA I */}
            <Box args={[0.12, 0.6, 0.05]} position={[-0.3, 0, 0]}>
                {neonMaterial}
            </Box>

            {/* LETRA F */}
            <group position={[0.2, 0, 0]}>
                {/* Haste Vertical */}
                <Box args={[0.12, 0.6, 0.05]} position={[0, 0, 0]}>
                    {neonMaterial}
                </Box>
                {/* Haste Superior */}
                <Box args={[0.25, 0.12, 0.05]} position={[0.18, 0.24, 0]}>
                    {neonMaterial}
                </Box>
                {/* Haste Meio */}
                <Box args={[0.18, 0.12, 0.05]} position={[0.14, 0.02, 0]}>
                    {neonMaterial}
                </Box>
            </group>

        </group>
    );
}

// --- O NÚCLEO (Anéis + Logo) ---
function CleanCore() {
  const groupRef = useRef();
  const ring1Ref = useRef();
  const ring2Ref = useRef();
  const ring3Ref = useRef();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();

    // Rotação suave dos anéis
    // Anel externo (Lento)
    if(ring1Ref.current) {
        ring1Ref.current.rotation.x = Math.sin(t * 0.5) * 0.2;
        ring1Ref.current.rotation.y = t * 0.2;
    }
    // Anel médio (Médio)
    if(ring2Ref.current) {
        ring2Ref.current.rotation.x = t * 0.4;
        ring2Ref.current.rotation.z = Math.cos(t * 0.5) * 0.2;
    }
    // Anel interno (Rápido)
    if(ring3Ref.current) {
        ring3Ref.current.rotation.y = t * 0.8;
        ring3Ref.current.rotation.x = Math.PI / 2; // Fica deitado girando
    }

    // O Grupo inteiro flutua levemente para dar vida
    groupRef.current.rotation.y = Math.sin(t * 0.2) * 0.1;
  });

  return (
    <group ref={groupRef} scale={1.2}>
        
        {/* O Logo Central */}
        <GeometricLogo />

        {/* Anel Externo (Azul Cyan) */}
        <group ref={ring1Ref}>
            <Torus args={[1.6, 0.02, 16, 64]}>
                <meshStandardMaterial color="#06b6d4" emissive="#06b6d4" emissiveIntensity={2} toneMapped={false} />
            </Torus>
        </group>

        {/* Anel Médio (Roxo Neon - Para contraste) */}
        <group ref={ring2Ref} rotation={[0.5, 0, 0]}>
            <Torus args={[1.3, 0.02, 16, 64]}>
                <meshStandardMaterial color="#d946ef" emissive="#d946ef" emissiveIntensity={2} toneMapped={false} />
            </Torus>
        </group>

        {/* Anel Interno (Branco Energia) */}
        <group ref={ring3Ref}>
            <Torus args={[0.9, 0.015, 16, 64]}>
                <meshStandardMaterial color="#ffffff" emissive="#ffffff" emissiveIntensity={1} toneMapped={false} />
            </Torus>
        </group>

    </group>
  );
}

export default function CyberMascot() {
  return (
    // IMPORTANTE: Removemos qualquer cor de fundo no CSS e forçamos transparência
    <div className="w-full h-full relative" style={{ background: 'transparent' }}> 
      
      <Canvas 
        camera={{ position: [0, 0, 5] }} 
        gl={{ alpha: true, antialias: true }} // Alpha true é vital
        onCreated={({ gl }) => { 
            gl.setClearColor(0x000000, 0); // Força transparência absoluta no renderizador
        }}
        dpr={[1, 1.5]} // Qualidade da imagem
      >
        
        {/* Luzes para dar volume 3D aos anéis */}
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#22d3ee" />
        <pointLight position={[-10, -10, -10]} intensity={1} color="#d946ef" />

        {/* Flutuação Geral */}
        <Float speed={2} rotationIntensity={0.2} floatIntensity={0.2}>
            <CleanCore />
        </Float>

        {/* Pós-processamento: Apenas Bloom (Brilho), configurado para não bugar transparência */}
        <EffectComposer multisampling={0} enabled={true}>
            <Bloom 
                intensity={1.5} 
                luminanceThreshold={0.2} 
                luminanceSmoothing={0.9} 
                radius={0.6} 
            />
        </EffectComposer>

      </Canvas>
    </div>
  );
}