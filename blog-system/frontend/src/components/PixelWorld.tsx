// @ts-expect-error - React is needed for JSX
import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

export function PixelWorld() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene>(new THREE.Scene());
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);

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
    // Keep renderer in scope

    // Create camera
    const camera = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.z = 5;
    cameraRef.current = camera;

    // Create pixel world
    const scene = sceneRef.current;
    scene.background = new THREE.Color(0x000000);

    // Create voxel city
    const cityGeometry = new THREE.BoxGeometry(1, 1, 1);
    const cityMaterial = new THREE.MeshPhongMaterial({
      color: 0x00ff00,
      flatShading: true,
    });

    // Create buildings
    for (let i = 0; i < 50; i++) {
      const building = new THREE.Mesh(cityGeometry, cityMaterial);
      const height = Math.random() * 2 + 0.5;
      building.scale.y = height;
      building.position.x = Math.random() * 10 - 5;
      building.position.z = Math.random() * 10 - 5;
      building.position.y = height / 2;
      scene.add(building);
    }

    // Add lights
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    // Animation loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (camera && newRenderer) {
        // Rotate camera around scene
        const time = Date.now() * 0.001;
        camera.position.x = Math.cos(time * 0.5) * 8;
        camera.position.z = Math.sin(time * 0.5) * 8;
        camera.lookAt(scene.position);
        
        newRenderer.render(scene, camera);
      }
    };
    animate();

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current || !camera || !newRenderer) return;
      
      camera.aspect = containerRef.current.clientWidth / containerRef.current.clientHeight;
      camera.updateProjectionMatrix();
      newRenderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
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
      aria-label="3D pixel art city visualization"
    />
  );
}
