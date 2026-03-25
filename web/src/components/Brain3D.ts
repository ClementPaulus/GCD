/**
 * Brain3D — Interactive Three.js 3D Brain Model
 *
 * Renders 52 anatomical brain structures as positioned 3D shapes
 * in a sagittal-to-3D mapping. Each region is clickable and color-coded
 * by category (cortical, subcortical, limbic, brainstem, cerebellar,
 * white_matter, specialized).
 *
 * Kernel data is computed live — F, ω, IC, Δ, S, C per structure.
 */

import * as THREE from 'three';

// ── Category Colors (hex) ────────────────────────────────────────

const CAT_HEX: Record<string, number> = {
  cortical: 0x3b82f6,
  subcortical: 0xa855f7,
  limbic: 0x22c55e,
  brainstem: 0xf59e0b,
  cerebellar: 0x06b6d4,
  white_matter: 0xec4899,
  specialized: 0xf43647,
};

// ── Neural Pathway Definitions ───────────────────────────────────
// Each pathway connects named regions with a color and label.

interface PathwayDef {
  name: string;
  label: string;
  color: number;
  regions: string[]; // ordered route through brain
}

const PATHWAYS: PathwayDef[] = [
  // ── Sensory ────────────────────────────────────────────────────
  {
    name: 'visual',
    label: 'Visual Pathway',
    color: 0x60a5fa,
    regions: ['lateral_geniculate', 'thalamic_pulvinar', 'occipital_cortex'],
  },
  {
    name: 'auditory',
    label: 'Auditory Pathway',
    color: 0x34d399,
    regions: ['medial_geniculate', 'temporal_cortex'],
  },
  {
    name: 'somatosensory',
    label: 'Somatosensory Pathway',
    color: 0x93c5fd,
    regions: ['medulla', 'thalamus', 'somatosensory_cortex', 'parietal_cortex'],
  },

  // ── Motor ──────────────────────────────────────────────────────
  {
    name: 'motor',
    label: 'Motor (Cortico-Basal Ganglia)',
    color: 0xc084fc,
    regions: ['frontal_cortex', 'putamen', 'globus_pallidus', 'thalamus', 'corticospinal_tract'],
  },
  {
    name: 'direct_pathway',
    label: 'Basal Ganglia Direct Pathway',
    color: 0xa78bfa,
    regions: ['frontal_cortex', 'caudate', 'putamen', 'globus_pallidus', 'thalamus', 'frontal_cortex'],
  },
  {
    name: 'indirect_pathway',
    label: 'Basal Ganglia Indirect Pathway',
    color: 0x7c3aed,
    regions: ['caudate', 'putamen', 'globus_pallidus', 'subthalamic_nucleus', 'globus_pallidus', 'thalamus'],
  },
  {
    name: 'cerebellar',
    label: 'Cerebellar Loop',
    color: 0x22d3ee,
    regions: ['frontal_cortex', 'pons', 'cerebellum_anterior', 'dentate_nucleus', 'cerebellar_peduncles', 'thalamus', 'frontal_cortex'],
  },
  {
    name: 'rubrospinal',
    label: 'Rubrospinal Tract',
    color: 0xd946ef,
    regions: ['red_nucleus', 'cerebellar_peduncles', 'corticospinal_tract', 'medulla'],
  },

  // ── Memory & Limbic ────────────────────────────────────────────
  {
    name: 'papez',
    label: 'Papez Circuit (Memory)',
    color: 0xfbbf24,
    regions: ['hippocampus_ca1', 'fornix', 'mammillary_body', 'mammillothalamic_tract', 'thalamus', 'cingulate_cortex', 'entorhinal_cortex', 'hippocampus_ca1'],
  },
  {
    name: 'hippocampal_entorhinal',
    label: 'Hippocampal-Entorhinal Loop',
    color: 0xfcd34d,
    regions: ['entorhinal_cortex', 'hippocampus_ca1', 'hippocampus_ca23', 'fornix', 'septal_nuclei'],
  },
  {
    name: 'prefrontal_amygdala',
    label: 'Prefrontal-Amygdala Regulation',
    color: 0xf0abfc,
    regions: ['prefrontal_dorsolateral', 'cingulate_cortex', 'amygdala_lateral', 'amygdala_basal', 'hypothalamus'],
  },

  // ── Reward & Motivation ────────────────────────────────────────
  {
    name: 'reward',
    label: 'Mesolimbic Reward Pathway',
    color: 0xf472b6,
    regions: ['midbrain', 'nucleus_accumbens', 'septal_nuclei', 'prefrontal_dorsolateral'],
  },

  // ── Large-Scale Networks ───────────────────────────────────────
  {
    name: 'salience',
    label: 'Salience Network',
    color: 0xfb923c,
    regions: ['insular_cortex', 'cingulate_cortex', 'amygdala_lateral', 'thalamus'],
  },
  {
    name: 'default_mode',
    label: 'Default Mode Network',
    color: 0x818cf8,
    regions: ['prefrontal_dorsolateral', 'cingulate_cortex', 'parietal_cortex', 'temporal_cortex', 'hippocampus_ca1'],
  },
  {
    name: 'frontoparietal',
    label: 'Frontoparietal Control Network',
    color: 0x67e8f9,
    regions: ['prefrontal_dorsolateral', 'parietal_cortex', 'insular_cortex', 'thalamus'],
  },

  // ── Language ───────────────────────────────────────────────────
  {
    name: 'language_arcuate',
    label: 'Language (Arcuate Fasciculus)',
    color: 0xe879f9,
    regions: ['frontal_cortex', 'arcuate_fasciculus', 'temporal_cortex', 'parietal_cortex'],
  },

  // ── Commissural & Association ──────────────────────────────────
  {
    name: 'callosal',
    label: 'Callosal Interhemispheric',
    color: 0xfda4af,
    regions: ['frontal_cortex', 'corpus_callosum', 'parietal_cortex', 'occipital_cortex'],
  },
  {
    name: 'limbic_thalamocortical',
    label: 'Limbic-Thalamo-Cortical',
    color: 0x86efac,
    regions: ['amygdala_lateral', 'thalamus', 'cingulate_cortex', 'prefrontal_dorsolateral', 'insular_cortex'],
  },

  // ── Neuromodulatory ────────────────────────────────────────────
  {
    name: 'dopamine',
    label: 'Dopaminergic (Nigrostriatal + Mesocortical)',
    color: 0xa78bfa,
    regions: ['substantia_nigra', 'putamen', 'caudate', 'nucleus_accumbens', 'frontal_cortex'],
  },
  {
    name: 'serotonin',
    label: 'Serotonergic Pathway',
    color: 0x2dd4bf,
    regions: ['raphe_nuclei', 'thalamus', 'hippocampus_ca1', 'amygdala_lateral', 'frontal_cortex', 'cingulate_cortex'],
  },
  {
    name: 'norepinephrine',
    label: 'Noradrenergic Pathway',
    color: 0xf87171,
    regions: ['locus_coeruleus', 'thalamus', 'amygdala_lateral', 'hippocampus_ca1', 'frontal_cortex'],
  },

  // ── Autonomic / Circadian ──────────────────────────────────────
  {
    name: 'circadian',
    label: 'Circadian (SCN → Pineal)',
    color: 0xfde68a,
    regions: ['suprachiasmatic_nucleus', 'hypothalamus', 'pineal_gland'],
  },
  {
    name: 'autonomic',
    label: 'Central Autonomic Network',
    color: 0xfda4af,
    regions: ['hypothalamus', 'amygdala_basal', 'insular_cortex', 'pons', 'medulla'],
  },
];

// ── Brain Region 3D Layout ───────────────────────────────────────
// Positions in normalized [-1, 1] brain space (sagittal view → 3D):
//   x = left-right (0 = midline)
//   y = superior-inferior
//   z = anterior-posterior

interface RegionDef {
  name: string;
  category: string;
  pos: [number, number, number]; // [x, y, z]
  scale: [number, number, number]; // [sx, sy, sz]
  shape: 'sphere' | 'ellipsoid' | 'capsule';
}

const REGION_DEFS: RegionDef[] = [
  // ── Cortical (8) ───────────────────────────────────────────────
  // Frontal lobe: anterior-superior, broad shell
  { name: 'frontal_cortex', category: 'cortical', pos: [0, 0.50, 0.55], scale: [0.50, 0.30, 0.30], shape: 'ellipsoid' },
  // Parietal lobe: superior-posterior to frontal, behind central sulcus
  { name: 'parietal_cortex', category: 'cortical', pos: [0, 0.62, -0.10], scale: [0.45, 0.22, 0.28], shape: 'ellipsoid' },
  // Occipital lobe: posterior pole
  { name: 'occipital_cortex', category: 'cortical', pos: [0, 0.30, -0.62], scale: [0.30, 0.25, 0.20], shape: 'ellipsoid' },
  // Temporal lobe: lateral-inferior, runs anterior-posterior
  { name: 'temporal_cortex', category: 'cortical', pos: [0.48, -0.05, 0.10], scale: [0.18, 0.18, 0.38], shape: 'ellipsoid' },
  // Insula: buried deep in lateral sulcus
  { name: 'insular_cortex', category: 'cortical', pos: [0.32, 0.12, 0.12], scale: [0.06, 0.12, 0.14], shape: 'ellipsoid' },
  // Entorhinal: medial temporal, anterior to hippocampus
  { name: 'entorhinal_cortex', category: 'cortical', pos: [0.18, -0.15, 0.18], scale: [0.07, 0.05, 0.07], shape: 'sphere' },
  // DLPFC: dorsolateral prefrontal, anterior-superior-lateral
  { name: 'prefrontal_dorsolateral', category: 'cortical', pos: [0.30, 0.55, 0.50], scale: [0.18, 0.14, 0.14], shape: 'ellipsoid' },
  // Somatosensory: postcentral gyrus, just behind central sulcus
  { name: 'somatosensory_cortex', category: 'cortical', pos: [0.18, 0.62, 0.02], scale: [0.14, 0.20, 0.10], shape: 'ellipsoid' },

  // ── Subcortical (7) ────────────────────────────────────────────
  // Thalamus: central relay, slightly posterior, near midline
  { name: 'thalamus', category: 'subcortical', pos: [0.06, 0.12, -0.06], scale: [0.14, 0.09, 0.11], shape: 'ellipsoid' },
  // Caudate: C-shaped, head anterior-superior to thalamus
  { name: 'caudate', category: 'subcortical', pos: [0.12, 0.30, 0.18], scale: [0.05, 0.14, 0.06], shape: 'ellipsoid' },
  // Putamen: lateral to globus pallidus
  { name: 'putamen', category: 'subcortical', pos: [0.22, 0.18, 0.08], scale: [0.06, 0.11, 0.08], shape: 'ellipsoid' },
  // Globus pallidus: medial to putamen
  { name: 'globus_pallidus', category: 'subcortical', pos: [0.16, 0.15, 0.04], scale: [0.04, 0.07, 0.05], shape: 'ellipsoid' },
  // Subthalamic nucleus: below thalamus, above substantia nigra
  { name: 'subthalamic_nucleus', category: 'subcortical', pos: [0.08, 0.02, -0.02], scale: [0.03, 0.02, 0.03], shape: 'sphere' },
  // Nucleus accumbens: ventral striatum, anterior-inferior
  { name: 'nucleus_accumbens', category: 'subcortical', pos: [0.08, 0.05, 0.25], scale: [0.04, 0.03, 0.04], shape: 'sphere' },
  // Claustrum: thin sheet lateral to putamen, deep to insula
  { name: 'claustrum', category: 'subcortical', pos: [0.28, 0.18, 0.10], scale: [0.02, 0.12, 0.10], shape: 'ellipsoid' },

  // ── Limbic (7) ─────────────────────────────────────────────────
  // Hippocampus CA1: medial temporal floor, curves posterior
  { name: 'hippocampus_ca1', category: 'limbic', pos: [0.18, -0.06, -0.08], scale: [0.06, 0.04, 0.12], shape: 'ellipsoid' },
  // Hippocampus CA2/3: slightly medial and posterior to CA1
  { name: 'hippocampus_ca23', category: 'limbic', pos: [0.16, -0.06, -0.18], scale: [0.05, 0.04, 0.10], shape: 'ellipsoid' },
  // Lateral amygdala: anterior medial temporal, superior
  { name: 'amygdala_lateral', category: 'limbic', pos: [0.20, -0.05, 0.10], scale: [0.05, 0.05, 0.04], shape: 'sphere' },
  // Basal amygdala: just inferior to lateral
  { name: 'amygdala_basal', category: 'limbic', pos: [0.20, -0.10, 0.10], scale: [0.04, 0.04, 0.04], shape: 'sphere' },
  // Cingulate: arches over corpus callosum, midline
  { name: 'cingulate_cortex', category: 'limbic', pos: [0.0, 0.48, 0.10], scale: [0.06, 0.04, 0.38], shape: 'ellipsoid' },
  // Septal nuclei: anterior to thalamus, ventral to corpus callosum
  { name: 'septal_nuclei', category: 'limbic', pos: [0.0, 0.12, 0.25], scale: [0.04, 0.04, 0.03], shape: 'sphere' },
  // Mammillary body: base of hypothalamus, posterior
  { name: 'mammillary_body', category: 'limbic', pos: [0.03, -0.08, 0.0], scale: [0.03, 0.03, 0.03], shape: 'sphere' },

  // ── Brainstem (7) ──────────────────────────────────────────────
  // Midbrain (mesencephalon): superior brainstem, below thalamus
  { name: 'midbrain', category: 'brainstem', pos: [0, -0.10, -0.18], scale: [0.08, 0.06, 0.08], shape: 'ellipsoid' },
  // Pons: below midbrain, bulges anteriorly
  { name: 'pons', category: 'brainstem', pos: [0, -0.22, -0.16], scale: [0.10, 0.07, 0.10], shape: 'ellipsoid' },
  // Medulla oblongata: inferior brainstem, continuous with spinal cord
  { name: 'medulla', category: 'brainstem', pos: [0, -0.36, -0.18], scale: [0.07, 0.10, 0.07], shape: 'ellipsoid' },
  // Substantia nigra: ventral midbrain
  { name: 'substantia_nigra', category: 'brainstem', pos: [0.06, -0.08, -0.16], scale: [0.04, 0.02, 0.05], shape: 'sphere' },
  // Red nucleus: dorsal midbrain, slightly medial
  { name: 'red_nucleus', category: 'brainstem', pos: [0.03, -0.06, -0.18], scale: [0.025, 0.025, 0.025], shape: 'sphere' },
  // Locus coeruleus: dorsal pons, tiny bilateral nuclei
  { name: 'locus_coeruleus', category: 'brainstem', pos: [0.04, -0.20, -0.22], scale: [0.02, 0.015, 0.02], shape: 'sphere' },
  // Raphe nuclei: midline brainstem, spans midbrain→medulla
  { name: 'raphe_nuclei', category: 'brainstem', pos: [0, -0.18, -0.20], scale: [0.02, 0.10, 0.02], shape: 'ellipsoid' },

  // ── Cerebellar (6) ─────────────────────────────────────────────
  // Anterior lobe: superior cerebellum, behind pons
  { name: 'cerebellum_anterior', category: 'cerebellar', pos: [0, -0.18, -0.46], scale: [0.30, 0.10, 0.12], shape: 'ellipsoid' },
  // Posterior lobe: largest part, inferior-posterior
  { name: 'cerebellum_posterior', category: 'cerebellar', pos: [0, -0.30, -0.52], scale: [0.35, 0.14, 0.15], shape: 'ellipsoid' },
  // Vermis: midline strip connecting hemispheres
  { name: 'vermis', category: 'cerebellar', pos: [0, -0.24, -0.50], scale: [0.05, 0.12, 0.10], shape: 'ellipsoid' },
  // Dentate nucleus: deep cerebellar nucleus, lateral
  { name: 'dentate_nucleus', category: 'cerebellar', pos: [0.14, -0.24, -0.48], scale: [0.04, 0.04, 0.04], shape: 'sphere' },
  // Cerebellar white matter: arbor vitae
  { name: 'cerebellar_wm', category: 'cerebellar', pos: [0, -0.22, -0.46], scale: [0.20, 0.08, 0.08], shape: 'ellipsoid' },
  // Cerebellar peduncles: connect cerebellum to brainstem
  { name: 'cerebellar_peduncles', category: 'cerebellar', pos: [0.10, -0.20, -0.36], scale: [0.06, 0.04, 0.06], shape: 'ellipsoid' },

  // ── White Matter (8) ───────────────────────────────────────────
  // Corpus callosum: massive midline commissure connecting hemispheres
  { name: 'corpus_callosum', category: 'white_matter', pos: [0, 0.36, 0.02], scale: [0.08, 0.03, 0.36], shape: 'ellipsoid' },
  // Corticospinal tract: descends from motor cortex through internal capsule to spinal cord
  { name: 'corticospinal_tract', category: 'white_matter', pos: [0.10, 0.05, -0.08], scale: [0.03, 0.30, 0.03], shape: 'ellipsoid' },
  // Arcuate fasciculus: connects Broca's area (frontal) to Wernicke's (temporal-parietal)
  { name: 'arcuate_fasciculus', category: 'white_matter', pos: [0.35, 0.32, 0.05], scale: [0.03, 0.03, 0.22], shape: 'ellipsoid' },
  // Uncinate fasciculus: connects anterior temporal to orbitofrontal
  { name: 'uncinate_fasciculus', category: 'white_matter', pos: [0.28, 0.02, 0.30], scale: [0.03, 0.03, 0.14], shape: 'ellipsoid' },
  // Fornix: arches from hippocampus to mammillary body
  { name: 'fornix', category: 'white_matter', pos: [0.04, 0.22, 0.0], scale: [0.03, 0.14, 0.05], shape: 'ellipsoid' },
  // Internal capsule: V-shaped fiber bundle between thalamus and basal ganglia
  { name: 'internal_capsule', category: 'white_matter', pos: [0.14, 0.18, -0.02], scale: [0.04, 0.16, 0.04], shape: 'ellipsoid' },
  // Anterior commissure: small commissure connecting temporal lobes anterior to fornix
  { name: 'anterior_commissure', category: 'white_matter', pos: [0, 0.08, 0.18], scale: [0.12, 0.02, 0.02], shape: 'ellipsoid' },
  // Cingulum bundle: runs within cingulate gyrus, connects frontal to temporal
  { name: 'cingulum_bundle', category: 'white_matter', pos: [0.06, 0.44, 0.06], scale: [0.03, 0.03, 0.32], shape: 'ellipsoid' },

  // ── Specialized (9) ────────────────────────────────────────────
  // Hypothalamus: ventral diencephalon, below thalamus
  { name: 'hypothalamus', category: 'specialized', pos: [0, -0.02, 0.08], scale: [0.06, 0.05, 0.06], shape: 'ellipsoid' },
  // Pulvinar: posterior thalamic nucleus, visual association
  { name: 'thalamic_pulvinar', category: 'specialized', pos: [0.08, 0.12, -0.18], scale: [0.06, 0.04, 0.05], shape: 'ellipsoid' },
  // LGN: lateral geniculate, inferolateral thalamus—visual relay
  { name: 'lateral_geniculate', category: 'specialized', pos: [0.14, 0.04, -0.12], scale: [0.03, 0.03, 0.03], shape: 'sphere' },
  // MGN: medial geniculate, posterior-inferior thalamus—auditory relay
  { name: 'medial_geniculate', category: 'specialized', pos: [0.10, 0.02, -0.15], scale: [0.025, 0.025, 0.025], shape: 'sphere' },
  // Mammillothalamic tract: vertical from mammillary body to anterior thalamus
  { name: 'mammillothalamic_tract', category: 'specialized', pos: [0.02, 0.02, 0.0], scale: [0.015, 0.08, 0.015], shape: 'ellipsoid' },
  // Pineal gland: dorsal midline, posterior to third ventricle
  { name: 'pineal_gland', category: 'specialized', pos: [0, 0.18, -0.20], scale: [0.025, 0.025, 0.025], shape: 'sphere' },
  // Choroid plexus: lines ventricles, primary in lateral ventricles
  { name: 'choroid_plexus', category: 'specialized', pos: [0.05, 0.28, -0.06], scale: [0.04, 0.02, 0.15], shape: 'ellipsoid' },
  // Area postrema: dorsal medulla, circumventricular organ (emetic trigger)
  { name: 'area_postrema', category: 'specialized', pos: [0, -0.34, -0.20], scale: [0.02, 0.015, 0.02], shape: 'sphere' },
  // SCN: suprachiasmatic nucleus, anterior hypothalamus above optic chiasm
  { name: 'suprachiasmatic_nucleus', category: 'specialized', pos: [0, -0.02, 0.14], scale: [0.02, 0.015, 0.02], shape: 'sphere' },
];

// ── Brain3D class ────────────────────────────────────────────────

export interface Brain3DOptions {
  canvas?: HTMLCanvasElement;
  container: HTMLElement;
  onRegionClick?: (regionName: string) => void;
  onRegionHover?: (regionName: string | null) => void;
}

type ColorMode = 'category' | 'fidelity' | 'drift' | 'integrity';

export class Brain3D {
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private regionMeshes: Map<string, THREE.Mesh> = new Map();
  private mirrorMeshes: Map<string, THREE.Mesh> = new Map();
  private pathwayLines: Map<string, THREE.Line> = new Map();
  private brainGroup: THREE.Group;
  private raycaster = new THREE.Raycaster();
  private mouse = new THREE.Vector2();
  private hoveredMesh: THREE.Mesh | null = null;
  private selectedName: string | null = null;
  private autoRotate = true;
  private isDragging = false;
  private prevMouse = { x: 0, y: 0 };
  private rotationSpeed = { x: 0, y: 0 };
  private animFrame = 0;
  private onRegionClick?: (name: string) => void;
  private onRegionHover?: (name: string | null) => void;
  private container: HTMLElement;
  private colorMode: ColorMode = 'category';
  private activePathways: Set<string> = new Set();
  private tooltip: HTMLDivElement | null = null;
  // Kernel data for heatmap modes (set externally)
  private kernelData: Map<string, { F: number; omega: number; IC: number; delta: number }> = new Map();

  constructor(opts: Brain3DOptions) {
    this.container = opts.container;
    this.onRegionClick = opts.onRegionClick;
    this.onRegionHover = opts.onRegionHover;

    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x020617);

    // Camera
    const aspect = opts.container.clientWidth / opts.container.clientHeight;
    this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 100);
    this.camera.position.set(1.8, 0.6, 1.8);
    this.camera.lookAt(0, 0.1, 0);

    // Renderer — use provided canvas or create one
    const rendererOpts: THREE.WebGLRendererParameters = { antialias: true, alpha: true };
    if (opts.canvas) rendererOpts.canvas = opts.canvas;
    this.renderer = new THREE.WebGLRenderer(rendererOpts);
    this.renderer.setSize(opts.container.clientWidth, opts.container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    if (!opts.canvas) opts.container.appendChild(this.renderer.domElement);

    // Lights
    const ambient = new THREE.AmbientLight(0x334155, 1.2);
    this.scene.add(ambient);
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(3, 4, 2);
    this.scene.add(dirLight);
    const backLight = new THREE.DirectionalLight(0x4488ff, 0.3);
    backLight.position.set(-2, -1, -3);
    this.scene.add(backLight);

    // Brain group (all regions)
    this.brainGroup = new THREE.Group();
    this.scene.add(this.brainGroup);

    // Create tooltip
    this.tooltip = document.createElement('div');
    this.tooltip.className = 'absolute pointer-events-none bg-kernel-950/95 border border-kernel-600 rounded px-2 py-1 text-[10px] text-kernel-300 hidden z-50';
    this.container.style.position = 'relative';
    this.container.appendChild(this.tooltip);

    // Build components
    this.buildOutline();
    this.buildRegions();
    this.buildPathways();

    // Events
    this.setupEvents();

    // Start animation
    this.animate();
  }

  private buildOutline(): void {
    // Semi-transparent cerebral outline (two hemispheres)
    const brainGeo = new THREE.SphereGeometry(0.85, 32, 24);
    brainGeo.scale(0.65, 0.55, 0.75);
    const brainMat = new THREE.MeshPhongMaterial({
      color: 0x1e293b,
      transparent: true,
      opacity: 0.08,
      wireframe: false,
      side: THREE.DoubleSide,
      depthWrite: false,
    });
    const outline = new THREE.Mesh(brainGeo, brainMat);
    outline.position.set(0, 0.2, 0);
    this.brainGroup.add(outline);

    // Spinal cord stump
    const spinalGeo = new THREE.CylinderGeometry(0.04, 0.03, 0.3, 8);
    const spinalMat = new THREE.MeshPhongMaterial({
      color: 0x334155,
      transparent: true,
      opacity: 0.15,
    });
    const spinal = new THREE.Mesh(spinalGeo, spinalMat);
    spinal.position.set(0, -0.5, -0.2);
    this.brainGroup.add(spinal);
  }

  private buildRegions(): void {
    for (const def of REGION_DEFS) {
      const color = CAT_HEX[def.category] ?? 0xffffff;

      // Create geometry
      const geo = new THREE.SphereGeometry(1, 16, 12);
      geo.scale(def.scale[0], def.scale[1], def.scale[2]);

      const mat = new THREE.MeshPhongMaterial({
        color,
        transparent: true,
        opacity: 0.55,
        emissive: new THREE.Color(color),
        emissiveIntensity: 0.15,
        shininess: 60,
      });

      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(def.pos[0], def.pos[1], def.pos[2]);
      mesh.userData = { regionName: def.name, category: def.category };
      this.brainGroup.add(mesh);
      this.regionMeshes.set(def.name, mesh);

      // Mirror for bilateral structures (those not on midline)
      if (Math.abs(def.pos[0]) > 0.01) {
        const mirrorMat = mat.clone();
        const mirrorMesh = new THREE.Mesh(geo.clone(), mirrorMat);
        mirrorMesh.position.set(-def.pos[0], def.pos[1], def.pos[2]);
        mirrorMesh.userData = { regionName: def.name, category: def.category, mirror: true };
        this.brainGroup.add(mirrorMesh);
        this.mirrorMeshes.set(def.name, mirrorMesh);
      }
    }
  }

  private buildPathways(): void {
    for (const pw of PATHWAYS) {
      const points: THREE.Vector3[] = [];
      for (const rname of pw.regions) {
        const mesh = this.regionMeshes.get(rname);
        if (mesh) points.push(mesh.position.clone());
      }
      if (points.length < 2) continue;

      // Create smooth curve through region centers
      const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
      const curvePoints = curve.getPoints(points.length * 12);
      const geo = new THREE.BufferGeometry().setFromPoints(curvePoints);
      const mat = new THREE.LineBasicMaterial({
        color: pw.color,
        transparent: true,
        opacity: 0.0, // hidden by default
        linewidth: 2,
      });
      const line = new THREE.Line(geo, mat);
      line.userData = { pathwayName: pw.name };
      this.brainGroup.add(line);
      this.pathwayLines.set(pw.name, line);
    }
  }

  private setupEvents(): void {
    const canvas = this.renderer.domElement;

    canvas.addEventListener('mousemove', (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      this.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      this.lastMouseEvent = { clientX: e.clientX, clientY: e.clientY };

      if (this.isDragging) {
        const dx = e.clientX - this.prevMouse.x;
        const dy = e.clientY - this.prevMouse.y;
        this.rotationSpeed.x = dx * 0.005;
        this.rotationSpeed.y = dy * 0.005;
        this.brainGroup.rotation.y += this.rotationSpeed.x;
        this.brainGroup.rotation.x += this.rotationSpeed.y;
        this.brainGroup.rotation.x = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, this.brainGroup.rotation.x));
        this.prevMouse = { x: e.clientX, y: e.clientY };
      }
    });

    canvas.addEventListener('mousedown', (e: MouseEvent) => {
      this.isDragging = true;
      this.autoRotate = false;
      this.prevMouse = { x: e.clientX, y: e.clientY };
    });

    canvas.addEventListener('mouseup', () => {
      this.isDragging = false;
    });

    canvas.addEventListener('mouseleave', () => {
      this.isDragging = false;
    });

    canvas.addEventListener('click', () => {
      if (Math.abs(this.rotationSpeed.x) > 0.02 || Math.abs(this.rotationSpeed.y) > 0.02) return;
      this.raycaster.setFromCamera(this.mouse, this.camera);
      const intersects = this.raycaster.intersectObjects(this.brainGroup.children, false);
      for (const hit of intersects) {
        const name = hit.object.userData?.regionName;
        if (name) {
          this.selectRegion(name);
          this.onRegionClick?.(name);
          break;
        }
      }
    });

    canvas.addEventListener('wheel', (e: WheelEvent) => {
      e.preventDefault();
      const dir = new THREE.Vector3();
      this.camera.getWorldDirection(dir);
      this.camera.position.addScaledVector(dir, -e.deltaY * 0.002);
      // Clamp distance
      const dist = this.camera.position.length();
      if (dist < 1.2) this.camera.position.setLength(1.2);
      if (dist > 5) this.camera.position.setLength(5);
    }, { passive: false });

    // Resize
    const ro = new ResizeObserver(() => {
      const w = this.container.clientWidth;
      const h = this.container.clientHeight;
      this.camera.aspect = w / h;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(w, h);
    });
    ro.observe(this.container);
  }

  private lastMouseEvent: { clientX: number; clientY: number } | null = null;

  private animate = (): void => {
    this.animFrame = requestAnimationFrame(this.animate);

    // Auto-rotate
    if (this.autoRotate) {
      this.brainGroup.rotation.y += 0.003;
    }

    // Gentle float
    this.brainGroup.position.y = Math.sin(Date.now() * 0.001) * 0.015;

    // Pulse active pathways
    for (const [name, line] of this.pathwayLines) {
      const mat = line.material as THREE.LineBasicMaterial;
      if (this.activePathways.has(name)) {
        mat.opacity = 0.5 + 0.3 * Math.sin(Date.now() * 0.003);
      }
    }

    // Raycast for hover
    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObjects(this.brainGroup.children, false);

    // Reset previous hover
    if (this.hoveredMesh) {
      const mat = this.hoveredMesh.material as THREE.MeshPhongMaterial;
      if (this.hoveredMesh.userData.regionName !== this.selectedName) {
        mat.emissiveIntensity = this.getBaseEmissive(this.hoveredMesh.userData.regionName);
        mat.opacity = this.getBaseOpacity(this.hoveredMesh.userData.regionName);
      }
      this.hoveredMesh = null;
    }

    let foundHover = false;
    for (const hit of intersects) {
      const name = hit.object.userData?.regionName;
      if (name) {
        this.hoveredMesh = hit.object as THREE.Mesh;
        const mat = this.hoveredMesh.material as THREE.MeshPhongMaterial;
        mat.emissiveIntensity = 0.5;
        mat.opacity = 0.85;
        this.onRegionHover?.(name);
        this.renderer.domElement.style.cursor = 'pointer';
        foundHover = true;

        // Update tooltip
        if (this.tooltip && this.lastMouseEvent) {
          const rect = this.container.getBoundingClientRect();
          const displayName = name.replace(/_/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase());
          const kd = this.kernelData.get(name);
          const extra = kd ? ` · F=${kd.F.toFixed(3)} · IC=${kd.IC.toFixed(3)}` : '';
          this.tooltip.textContent = `${displayName}${extra}`;
          this.tooltip.classList.remove('hidden');
          this.tooltip.style.left = `${this.lastMouseEvent.clientX - rect.left + 12}px`;
          this.tooltip.style.top = `${this.lastMouseEvent.clientY - rect.top - 20}px`;
        }
        break;
      }
    }

    if (!foundHover) {
      this.onRegionHover?.(null);
      this.renderer.domElement.style.cursor = this.isDragging ? 'grabbing' : 'grab';
      if (this.tooltip) this.tooltip.classList.add('hidden');
    }

    // Dampen rotation
    if (!this.isDragging) {
      this.rotationSpeed.x *= 0.95;
      this.rotationSpeed.y *= 0.95;
      this.brainGroup.rotation.y += this.rotationSpeed.x;
      this.brainGroup.rotation.x += this.rotationSpeed.y;
      this.brainGroup.rotation.x = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, this.brainGroup.rotation.x));
    }

    this.renderer.render(this.scene, this.camera);
  };

  private getBaseEmissive(name: string): number {
    if (this.selectedName && name !== this.selectedName) return 0.05;
    return 0.15;
  }

  private getBaseOpacity(name: string): number {
    if (this.selectedName && name !== this.selectedName) return 0.2;
    return 0.55;
  }

  // ── Public API ─────────────────────────────────────────────────

  selectRegion(name: string): void {
    this.selectedName = name;

    // Highlight selected, dim others
    this.regionMeshes.forEach((m, n) => {
      const mat = m.material as THREE.MeshPhongMaterial;
      if (n === name) {
        mat.emissiveIntensity = 0.7;
        mat.opacity = 0.9;
      } else {
        mat.opacity = 0.2;
        mat.emissiveIntensity = 0.05;
      }
    });

    // Also handle mirror meshes
    this.mirrorMeshes.forEach((m, n) => {
      const mat = m.material as THREE.MeshPhongMaterial;
      if (n === name) {
        mat.emissiveIntensity = 0.7;
        mat.opacity = 0.9;
      } else {
        mat.opacity = 0.2;
        mat.emissiveIntensity = 0.05;
      }
    });

    // Show pathways that include this region
    this.pathwayLines.forEach((line, pwName) => {
      const pw = PATHWAYS.find(p => p.name === pwName);
      const mat = line.material as THREE.LineBasicMaterial;
      if (pw && pw.regions.includes(name)) {
        mat.opacity = 0.6;
        // Also brighten other regions in this pathway
        for (const rn of pw.regions) {
          const rm = this.regionMeshes.get(rn);
          if (rm && rn !== name) {
            const rmat = rm.material as THREE.MeshPhongMaterial;
            rmat.opacity = 0.45;
            rmat.emissiveIntensity = 0.12;
          }
        }
      } else {
        mat.opacity = 0.0;
      }
    });
  }

  clearSelection(): void {
    this.selectedName = null;
    this.regionMeshes.forEach(m => {
      const mat = m.material as THREE.MeshPhongMaterial;
      mat.opacity = 0.55;
      mat.emissiveIntensity = 0.15;
    });
    this.mirrorMeshes.forEach(m => {
      const mat = m.material as THREE.MeshPhongMaterial;
      mat.opacity = 0.55;
      mat.emissiveIntensity = 0.15;
    });
    // Hide all pathways
    this.pathwayLines.forEach(line => {
      (line.material as THREE.LineBasicMaterial).opacity = 0.0;
    });
    this.applyColorMode();
  }

  /** Show/hide a specific neural pathway */
  togglePathway(pathwayName: string): boolean {
    if (this.activePathways.has(pathwayName)) {
      this.activePathways.delete(pathwayName);
      const line = this.pathwayLines.get(pathwayName);
      if (line) (line.material as THREE.LineBasicMaterial).opacity = 0.0;
      return false;
    } else {
      this.activePathways.add(pathwayName);
      const line = this.pathwayLines.get(pathwayName);
      if (line) (line.material as THREE.LineBasicMaterial).opacity = 0.6;
      return true;
    }
  }

  /** Show all pathways */
  showAllPathways(): void {
    for (const pw of PATHWAYS) {
      this.activePathways.add(pw.name);
      const line = this.pathwayLines.get(pw.name);
      if (line) (line.material as THREE.LineBasicMaterial).opacity = 0.5;
    }
  }

  /** Hide all pathways */
  hideAllPathways(): void {
    this.activePathways.clear();
    this.pathwayLines.forEach(line => {
      (line.material as THREE.LineBasicMaterial).opacity = 0.0;
    });
  }

  /** Filter visible regions by category */
  filterCategory(category: string | null): void {
    this.regionMeshes.forEach((m, n) => {
      const cat = m.userData.category;
      const show = !category || cat === category;
      const mat = m.material as THREE.MeshPhongMaterial;
      mat.opacity = show ? 0.55 : 0.06;
      mat.emissiveIntensity = show ? 0.15 : 0.02;
    });
    this.mirrorMeshes.forEach((m) => {
      const cat = m.userData.category;
      const show = !category || cat === category;
      const mat = m.material as THREE.MeshPhongMaterial;
      mat.opacity = show ? 0.55 : 0.06;
      mat.emissiveIntensity = show ? 0.15 : 0.02;
    });
  }

  /** Set kernel data for heatmap color modes */
  setKernelData(data: Map<string, { F: number; omega: number; IC: number; delta: number }>): void {
    this.kernelData = data;
  }

  /** Switch color mode: category colors, fidelity heatmap, drift heatmap, integrity heatmap */
  setColorMode(mode: ColorMode): void {
    this.colorMode = mode;
    this.applyColorMode();
  }

  private applyColorMode(): void {
    const mode = this.colorMode;

    this.regionMeshes.forEach((mesh, name) => {
      const mat = mesh.material as THREE.MeshPhongMaterial;
      if (mode === 'category') {
        mat.color.setHex(CAT_HEX[mesh.userData.category] ?? 0xffffff);
        mat.emissive.setHex(CAT_HEX[mesh.userData.category] ?? 0xffffff);
      } else {
        const kd = this.kernelData.get(name);
        if (!kd) return;
        let t = 0;
        if (mode === 'fidelity') t = kd.F;
        else if (mode === 'drift') t = kd.omega;
        else if (mode === 'integrity') t = kd.IC;
        const color = this.heatColor(t, mode === 'drift');
        mat.color.set(color);
        mat.emissive.set(color);
      }
    });

    // Apply to mirrors too
    this.mirrorMeshes.forEach((mesh) => {
      const name = mesh.userData.regionName;
      const mat = mesh.material as THREE.MeshPhongMaterial;
      if (mode === 'category') {
        mat.color.setHex(CAT_HEX[mesh.userData.category] ?? 0xffffff);
        mat.emissive.setHex(CAT_HEX[mesh.userData.category] ?? 0xffffff);
      } else {
        const kd = this.kernelData.get(name);
        if (!kd) return;
        let t = 0;
        if (mode === 'fidelity') t = kd.F;
        else if (mode === 'drift') t = kd.omega;
        else if (mode === 'integrity') t = kd.IC;
        const color = this.heatColor(t, mode === 'drift');
        mat.color.set(color);
        mat.emissive.set(color);
      }
    });
  }

  /** Green→Yellow→Red heatmap. For drift, red=high is bad. For F/IC, green=high is good */
  private heatColor(t: number, invertGood: boolean): THREE.Color {
    const v = Math.max(0, Math.min(1, t));
    if (invertGood) {
      // drift: low=green, high=red
      return new THREE.Color().setHSL((1 - v) * 0.33, 0.8, 0.45);
    }
    // F, IC: low=red, high=green
    return new THREE.Color().setHSL(v * 0.33, 0.8, 0.45);
  }

  /** Get list of available pathway names and labels */
  static getPathways(): { name: string; label: string; color: string }[] {
    return PATHWAYS.map(p => ({
      name: p.name,
      label: p.label,
      color: '#' + p.color.toString(16).padStart(6, '0'),
    }));
  }

  resetView(): void {
    this.autoRotate = true;
    this.brainGroup.rotation.set(0, 0, 0);
    this.camera.position.set(1.8, 0.6, 1.8);
    this.camera.lookAt(0, 0.1, 0);
    this.clearSelection();
  }

  dispose(): void {
    cancelAnimationFrame(this.animFrame);
    this.renderer.dispose();
    this.scene.clear();
    this.renderer.domElement.remove();
    if (this.tooltip) this.tooltip.remove();
  }
}
