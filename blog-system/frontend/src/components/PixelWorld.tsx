// @ts-expect-error - React is needed for JSX
import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass';

export function PixelWorld() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene>(new THREE.Scene());
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  // Define types for post-processing
  type PostProcessingPass = {
    dispose?: () => void;
  };
  
  const composerRef = useRef<{
    passes: PostProcessingPass[];
    render: () => void;
    setSize: (width: number, height: number) => void;
  } | null>(null);

  // Setup scene
  useEffect(() => {
    if (!containerRef.current) return;

    // Store container reference for cleanup
    const container = containerRef.current;
    
    // Create renderer with pixel effect
    const newRenderer = new THREE.WebGLRenderer({
      antialias: false, // Disable antialiasing for pixel effect
      powerPreference: "high-performance"
    });
    newRenderer.setPixelRatio(window.devicePixelRatio * 0.5); // Lower resolution for pixel effect
    newRenderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(newRenderer.domElement);

    // Create camera
    const camera = new THREE.PerspectiveCamera(
      75,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.z = 5;
    cameraRef.current = camera;

    // Create cyberpunk world with enhanced atmosphere
    const scene = sceneRef.current;
    scene.background = new THREE.Color(0x000913); // Deep blue-black for night sky
    
    // Add volumetric fog with neon tint
    const fogColor = new THREE.Color(0x000913);
    fogColor.lerp(new THREE.Color(0xff1493), 0.02); // Slight pink tint
    scene.fog = new THREE.FogExp2(fogColor, 0.035);
    
    // Add performance optimization hints
    scene.matrixAutoUpdate = false; // Manual matrix updates for static objects

    // Create cyberpunk buildings
    const cityGeometry = new THREE.BoxGeometry(1, 1, 1);
    const buildingMaterials = [
      new THREE.MeshPhongMaterial({
        color: 0x0a0a0a,
        emissive: 0x000000,
        specular: 0x111111,
        shininess: 30,
        flatShading: true,
      }),
      new THREE.MeshPhongMaterial({
        color: 0x0f0f0f,
        emissive: 0xff1493,
        emissiveIntensity: 0.5,
        specular: 0x111111,
        shininess: 30,
        flatShading: true,
      }),
      new THREE.MeshPhongMaterial({
        color: 0x0a0a0a,
        emissive: 0x00ffff,
        emissiveIntensity: 0.5,
        specular: 0x111111,
        shininess: 30,
        flatShading: true,
      })
    ];

    // Create cyberpunk buildings
    for (let i = 0; i < 100; i++) {
      const building = new THREE.Mesh(
        cityGeometry,
        buildingMaterials[Math.floor(Math.random() * buildingMaterials.length)]
      );
      const height = Math.random() * 4 + 1; // Taller buildings
      const width = Math.random() * 0.5 + 0.5;
      const depth = Math.random() * 0.5 + 0.5;
      
      building.scale.set(width, height, depth);
      building.position.x = Math.random() * 20 - 10;
      building.position.z = Math.random() * 20 - 10;
      building.position.y = height / 2;
      
      // Add random rotation for more organic feel
      building.rotation.y = Math.random() * Math.PI * 2;
      
      scene.add(building);
    }
    
    // Add ground plane with reflection
    const groundGeometry = new THREE.PlaneGeometry(100, 100);
    const groundMaterial = new THREE.MeshPhongMaterial({
      color: 0x0a0a0a,
      specular: 0x111111,
      shininess: 100,
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = 0;
    scene.add(ground);

    // Add enhanced cyberpunk lighting with volumetric effects
    const ambientLight = new THREE.AmbientLight(0x101010, 0.5);
    scene.add(ambientLight);
    
    // Add hemisphere light for better ambient occlusion
    const hemiLight = new THREE.HemisphereLight(0x000913, 0xff1493, 0.3);
    scene.add(hemiLight);

    // Add multiple colored lights for neon effect
    const lights: Array<{
      color: number;
      intensity: number;
      position: [number, number, number];
    }> = [
      { color: 0xff1493, intensity: 1, position: [5, 5, 5] },
      { color: 0x00ffff, intensity: 1, position: [-5, 5, -5] },
      { color: 0xff00ff, intensity: 0.5, position: [0, 10, 0] }
    ];

    lights.forEach(({ color, intensity, position }) => {
      const light = new THREE.PointLight(color, intensity, 20);
      light.position.set(...position);
      scene.add(light);
    });

    // Add post-processing effects
    const composer = new EffectComposer(newRenderer);
    composerRef.current = composer;

    const renderPass = new RenderPass(scene, camera);
    composer.addPass(renderPass);

    // Add bloom effect for neon glow with performance optimization
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(
        Math.min(window.innerWidth, 1024), // Limit resolution for better performance
        Math.min(window.innerHeight, 1024)
      ),
      2.0, // Increased bloom intensity for stronger neon effect
      0.5, // Slightly increased bloom radius
      0.2  // Lower threshold to make more elements glow
    );
    
    // Performance optimization: use selective bloom
    bloomPass.threshold = 0.2;
    bloomPass.strength = 2.0;
    bloomPass.radius = 0.5;
    composer.addPass(bloomPass);

    // Add final output pass
    const outputPass = new OutputPass();
    composer.addPass(outputPass);

    // Animation loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (camera) {
        // Rotate camera around scene
        const time = Date.now() * 0.001;
        camera.position.x = Math.cos(time * 0.5) * 8;
        camera.position.z = Math.sin(time * 0.5) * 8;
        camera.lookAt(scene.position);
        
        composerRef.current?.render();
      }
    };
    animate();

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current || !camera || !newRenderer) return;
      
      camera.aspect = containerRef.current.clientWidth / containerRef.current.clientHeight;
      camera.updateProjectionMatrix();
      newRenderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
      composerRef.current?.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup with proper disposal of resources
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      
      // Dispose of materials and geometries
      scene.traverse((object) => {
        if (object instanceof THREE.Mesh) {
          if (object.geometry) object.geometry.dispose();
          if (object.material) {
            if (Array.isArray(object.material)) {
              object.material.forEach(material => material.dispose());
            } else {
              object.material.dispose();
            }
          }
        }
      });
      
      // Dispose of post-processing effects
      if (composerRef.current) {
        composerRef.current.passes.forEach((pass: { dispose?: () => void }) => {
          if (pass.dispose) pass.dispose();
        });
      }
      
      // Dispose of renderer
      if (newRenderer && container) {
        newRenderer.dispose();
        container.removeChild(newRenderer.domElement);
      }
    };
  }, []);

  return (
    <div 
      ref={containerRef} 
      className="w-full h-96 bg-black"
      aria-label="3D cyberpunk city visualization"
    />
  );
}
