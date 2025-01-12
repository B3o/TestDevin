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

    // Create detailed cyberpunk buildings with neon edges
    const buildingGeometries = [
      new THREE.BoxGeometry(1, 1, 1),
      new THREE.CylinderGeometry(0.5, 0.5, 1, 8),
      new THREE.BoxGeometry(0.8, 1, 0.8)
    ];

    // Create holographic billboard geometry
    const billboardGeometry = new THREE.PlaneGeometry(2, 3);
    
    // Holographic shader material
    const holoShader = {
      uniforms: {
        time: { value: 0 },
        color: { value: new THREE.Color(0x00ffff) }
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform vec3 color;
        varying vec2 vUv;
        
        void main() {
          float scanline = sin(vUv.y * 50.0 + time * 2.0) * 0.15 + 0.85;
          float flicker = sin(time * 8.0) * 0.03 + 0.97;
          float noise = fract(sin(dot(vUv, vec2(12.9898,78.233))) * 43758.5453123);
          
          vec3 finalColor = color * scanline * flicker;
          float alpha = (0.6 + noise * 0.2) * (1.0 - pow(abs(vUv.x - 0.5) * 2.0, 2.0));
          
          gl_FragColor = vec4(finalColor, alpha);
        }
      `
    };

    const buildingMaterials = [
      // Base building material
      new THREE.MeshPhongMaterial({
        color: 0x0a0a0a,
        emissive: 0x000000,
        specular: 0x111111,
        shininess: 30,
        flatShading: true,
      }),
      // Neon edge material
      new THREE.MeshPhongMaterial({
        color: 0x0f0f0f,
        emissive: 0xff1493,
        emissiveIntensity: 2.0,
        specular: 0x111111,
        shininess: 30,
        flatShading: true,
      }),
      // Alternative neon material
      new THREE.MeshPhongMaterial({
        color: 0x0a0a0a,
        emissive: 0x00ffff,
        emissiveIntensity: 2.0,
        specular: 0x111111,
        shininess: 30,
        flatShading: true,
      })
    ];

    // Create holographic billboard material
    const holoMaterial = new THREE.ShaderMaterial({
      uniforms: holoShader.uniforms,
      vertexShader: holoShader.vertexShader,
      fragmentShader: holoShader.fragmentShader,
      transparent: true,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending
    });

    // Create cyberpunk buildings with billboards
    for (let i = 0; i < 100; i++) {
      // Create main building
      const geometryIndex = Math.floor(Math.random() * buildingGeometries.length);
      const building = new THREE.Mesh(
        buildingGeometries[geometryIndex],
        buildingMaterials[Math.floor(Math.random() * buildingMaterials.length)]
      );
      
      const height = Math.random() * 6 + 2; // Taller buildings
      const width = Math.random() * 0.8 + 0.5;
      const depth = Math.random() * 0.8 + 0.5;
      
      building.scale.set(width, height, depth);
      building.position.x = Math.random() * 20 - 10;
      building.position.z = Math.random() * 20 - 10;
      building.position.y = height / 2;
      building.rotation.y = Math.random() * Math.PI * 2;
      
      // Add neon edges using line segments
      const edges = new THREE.EdgesGeometry(building.geometry);
      const edgeMaterial = new THREE.LineBasicMaterial({ 
        color: Math.random() > 0.5 ? 0xff1493 : 0x00ffff,
        linewidth: 2
      });
      const edgeLines = new THREE.LineSegments(edges, edgeMaterial);
      building.add(edgeLines);
      
      // Add holographic billboard to some buildings
      if (Math.random() > 0.7) {
        const billboard = new THREE.Mesh(billboardGeometry, holoMaterial);
        billboard.position.y = height / 2;
        billboard.position.x = width / 2 + 0.1;
        billboard.rotation.y = Math.PI / 2;
        building.add(billboard);
        
        // Add another billboard on the opposite side
        const billboard2 = billboard.clone();
        billboard2.position.x = -width / 2 - 0.1;
        billboard2.rotation.y = -Math.PI / 2;
        building.add(billboard2);
      }
      
      scene.add(building);
    }
    
    // Add cyberpunk ground with glowing patterns
    const groundGeometry = new THREE.PlaneGeometry(100, 100, 50, 50);
    const groundShader = {
      uniforms: {
        time: { value: 0 },
        color1: { value: new THREE.Color(0x000913) },
        color2: { value: new THREE.Color(0x00ffff) }
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform vec3 color1;
        uniform vec3 color2;
        varying vec2 vUv;
        
        float grid(vec2 uv, float size) {
          vec2 grid = fract(uv * size);
          return step(0.95, max(grid.x, grid.y));
        }
        
        void main() {
          float gridPattern = grid(vUv, 50.0) * 0.5;
          float pulsePattern = sin(vUv.x * 20.0 + time) * 0.5 + 0.5;
          pulsePattern *= sin(vUv.y * 20.0 + time * 0.5) * 0.5 + 0.5;
          
          vec3 color = mix(color1, color2, gridPattern + pulsePattern * 0.3);
          gl_FragColor = vec4(color, 1.0);
        }
      `
    };
    
    const groundMaterial = new THREE.ShaderMaterial({
      uniforms: groundShader.uniforms,
      vertexShader: groundShader.vertexShader,
      fragmentShader: groundShader.fragmentShader
    });
    
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = 0;
    scene.add(ground);
    
    // Add neon pipes
    const createNeonPipe = () => {
      const curve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(Math.random() * 20 - 10, Math.random() * 10 + 5, Math.random() * 20 - 10),
        new THREE.Vector3(Math.random() * 20 - 10, Math.random() * 10 + 5, Math.random() * 20 - 10),
        new THREE.Vector3(Math.random() * 20 - 10, Math.random() * 10 + 5, Math.random() * 20 - 10),
        new THREE.Vector3(Math.random() * 20 - 10, Math.random() * 10 + 5, Math.random() * 20 - 10)
      ]);
      
      const tubeGeometry = new THREE.TubeGeometry(curve, 100, 0.1, 8, false);
      const tubeMaterial = new THREE.MeshPhongMaterial({
        color: 0x000000,
        emissive: Math.random() > 0.5 ? 0xff1493 : 0x00ffff,
        emissiveIntensity: 2.0,
        shininess: 100
      });
      
      return new THREE.Mesh(tubeGeometry, tubeMaterial);
    };
    
    // Add multiple neon pipes
    for (let i = 0; i < 15; i++) {
      scene.add(createNeonPipe());
    }
    
    // Add maglev train track
    const trackCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-15, 8, -15),
      new THREE.Vector3(-15, 8, 15),
      new THREE.Vector3(15, 8, 15),
      new THREE.Vector3(15, 8, -15),
      new THREE.Vector3(-15, 8, -15)
    ]);
    
    const trackGeometry = new THREE.TubeGeometry(trackCurve, 200, 0.2, 8, true);
    const trackMaterial = new THREE.MeshPhongMaterial({
      color: 0x101010,
      emissive: 0x39ff14,
      emissiveIntensity: 1.0,
      shininess: 100
    });
    
    const track = new THREE.Mesh(trackGeometry, trackMaterial);
    scene.add(track);
    
    // Add train
    const trainGeometry = new THREE.CapsuleGeometry(0.3, 2, 4, 8);
    const trainMaterial = new THREE.MeshPhongMaterial({
      color: 0x202020,
      emissive: 0x39ff14,
      emissiveIntensity: 0.5,
      shininess: 100
    });
    
    const train = new THREE.Mesh(trainGeometry, trainMaterial);
    scene.add(train);
    
    // Add drones
    const createDrone = () => {
      const droneGroup = new THREE.Group();
      
      // Drone body
      const body = new THREE.Mesh(
        new THREE.BoxGeometry(0.5, 0.2, 0.5),
        new THREE.MeshPhongMaterial({
          color: 0x202020,
          emissive: 0xff1493,
          emissiveIntensity: 0.5
        })
      );
      droneGroup.add(body);
      
      // Drone light beam
      const beamGeometry = new THREE.CylinderGeometry(0.1, 0.3, 2, 8);
      const beamMaterial = new THREE.MeshPhongMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.2,
        emissive: 0xffffff,
        emissiveIntensity: 1.0
      });
      const beam = new THREE.Mesh(beamGeometry, beamMaterial);
      beam.position.y = -1;
      droneGroup.add(beam);
      
      return droneGroup;
    };
    
    // Add multiple drones
    const drones = Array(5).fill(null).map(() => {
      const drone = createDrone();
      drone.position.set(
        Math.random() * 30 - 15,
        Math.random() * 5 + 10,
        Math.random() * 30 - 15
      );
      scene.add(drone);
      return drone;
    });

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
        const time = Date.now() * 0.001;
        
        // Update shader uniforms
        holoShader.uniforms.time.value = time;
        groundShader.uniforms.time.value = time;
        
        // Rotate camera around scene
        camera.position.x = Math.cos(time * 0.5) * 8;
        camera.position.z = Math.sin(time * 0.5) * 8;
        camera.lookAt(scene.position);
        
        // Update holographic billboards
        scene.traverse((object) => {
          if (object instanceof THREE.Mesh && object.material === holoMaterial) {
            object.material.uniforms.time.value = time;
          }
        });
        
        // Animate train along track
        if (train) {
          const trainProgress = (time * 0.2) % 1;
          const trainPosition = trackCurve.getPointAt(trainProgress);
          const trainTangent = trackCurve.getTangentAt(trainProgress);
          
          train.position.copy(trainPosition);
          train.quaternion.setFromUnitVectors(
            new THREE.Vector3(0, 0, 1),
            trainTangent
          );
        }
        
        // Animate drones
        drones.forEach((drone, i) => {
          const offset = i * Math.PI * 0.4;
          drone.position.y += Math.sin(time * 2 + offset) * 0.02;
          drone.rotation.y = time + offset;
        });
        
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
