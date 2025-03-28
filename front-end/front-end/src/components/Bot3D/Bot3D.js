import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { Boolean } from 'three-stdlib'; // Importamos el módulo Boolean
import './Bot3D.css';

const Bot3D = ({ isTyping }) => {
  const mountRef = useRef(null);
  const scene = useRef(null);
  const bot = useRef(null);
  const leftEye = useRef(null);
  const rightEye = useRef(null);
  const animationId = useRef(null);
  const mouse = useRef({ x: 0, y: 0 });

  useEffect(() => {
    // 1. Configuración inicial
    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;
    
    // Escena
    scene.current = new THREE.Scene();
    scene.current.background = new THREE.Color(0xf8f8f8);
    
    // Cámara
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 5;
    
    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    mountRef.current.appendChild(renderer.domElement);

    // 2. Crear modelo del bot - VERSIÓN SIMPLIFICADA SIN OPERACIONES BOOLEANAS
    const group = new THREE.Group();
    
    // Cabeza (esfera simple)
    const headGeometry = new THREE.SphereGeometry(0.8, 32, 32);
    const headMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x3cb371,
      roughness: 0.3,
      metalness: 0.2
    });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    group.add(head);
    
    // Ojos (esferas encima de la cabeza)
    const eyeGeometry = new THREE.SphereGeometry(0.1, 16, 16);
    const eyeMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xffffff,
      roughness: 0.1,
      metalness: 0.5
    });
    
    leftEye.current = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.current.position.set(-0.3, 0.2, 0.8);
    
    rightEye.current = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.current.position.set(0.3, 0.2, 0.8);
    
    // Pupilas
    const pupilGeometry = new THREE.SphereGeometry(0.04, 16, 16);
    const pupilMaterial = new THREE.MeshBasicMaterial({ color: 0x222222 });
    
    const leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    leftPupil.position.set(0, 0, 0.1);
    leftEye.current.add(leftPupil);
    
    const rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    rightPupil.position.set(0, 0, 0.1);
    rightEye.current.add(rightPupil);
    
    group.add(leftEye.current);
    group.add(rightEye.current);
    
    // Boca (toro semi-transparente)
    const mouthGeometry = new THREE.TorusGeometry(0.2, 0.03, 16, 32, Math.PI);
    const mouthMaterial = new THREE.MeshBasicMaterial({ 
      color: 0x222222,
      transparent: true,
      opacity: 0.8
    });
    const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
    mouth.position.set(0, -0.2, 0.8);
    mouth.rotation.x = Math.PI;
    group.add(mouth);
    
    // Torso
    const torsoGeometry = new THREE.CylinderGeometry(0.6, 0.5, 1.5, 6);
    const torsoMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x2e8b57,
      roughness: 0.4,
      metalness: 0.1
    });
    const torso = new THREE.Mesh(torsoGeometry, torsoMaterial);
    torso.position.y = -1.2;
    group.add(torso);
    
    // Cuello
    const neckGeometry = new THREE.CylinderGeometry(0.2, 0.3, 0.3, 8);
    const neckMaterial = new THREE.MeshStandardMaterial({ color: 0x3cb371 });
    const neck = new THREE.Mesh(neckGeometry, neckMaterial);
    neck.position.y = -0.5;
    group.add(neck);
    
    bot.current = group;
    scene.current.add(bot.current);

    // 3. Iluminación
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.current.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.current.add(directionalLight);
    
    const backLight = new THREE.DirectionalLight(0xffffff, 0.4);
    backLight.position.set(-1, -1, -1);
    scene.current.add(backLight);

    // 4. Seguimiento del cursor
    const handleMouseMove = (event) => {
      mouse.current.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.current.y = -(event.clientY / window.innerHeight) * 2 + 1;
    };
    
    window.addEventListener('mousemove', handleMouseMove);

    // 5. Animación
    const animate = () => {
      animationId.current = requestAnimationFrame(animate);
      
      // Rotación del bot sobre su eje
      bot.current.rotation.y += isTyping ? 0.02 : 0.005;
      
      // Seguimiento del cursor con los ojos
      if (leftEye.current && rightEye.current) {
        const eyeMovementRange = 0.1;
        
        leftEye.current.children[0].position.set(
          mouse.current.x * eyeMovementRange,
          mouse.current.y * eyeMovementRange,
          0.1
        );
        
        rightEye.current.children[0].position.set(
          mouse.current.x * eyeMovementRange,
          mouse.current.y * eyeMovementRange,
          0.1
        );
      }
      
      renderer.render(scene.current, camera);
    };
    
    animate();

    // 6. Limpieza
    return () => {
      cancelAnimationFrame(animationId.current);
      window.removeEventListener('mousemove', handleMouseMove);
      mountRef.current?.removeChild(renderer.domElement);
    };
  }, [isTyping]);

  return <div className="bot-3d" ref={mountRef} />;
};

export default Bot3D;