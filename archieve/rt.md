# Research Update
Peter Sun | Cornell University  
Nov 06, 2017  
<a href = "Research_Update20171106.html" style = "color:black; border-bottom: 0px;">Slide Version</a>

## Overview

### Graphene

- Monolayer
- Multilayer
    - Growth
    - Etch
    - Transfer
- Current progress

### Blender Animation

- General Pipeline
- Python Script
- AWS integration

# Graphene

## Graphene: Monolayer {#w100}

![Monolayer Graphene Transfer Attempts. Concentration of etchant varies, and One side of graphene cleaned with sandpaper or tape.](figures/monolayer1.png)  

## Graphene: Monolayer 

<br>

### $\bigotimes$ **NO** 

- Not robust on water or water/IPA surface
- Requires a extremely flat surface with a relatively large area

## Multi-Layer Graphene: Growth

[^Kim2009jan]: **Kim2009jan** Kim, K.S. et al. "Large-scale pattern growth of graphene films for stretchable transparent electrodes", *Nature Letter*, **2009**, *457*, 706-710 [10.1038/nature07719](https://doi.org/10.1038/nature07719)
[^Jo2010apr]: **Jo2010apr** Jo, G. et al. "Large-scale patterned multi-layer graphene films as transparent conducting electrodes for GaN light-emitting diodes", *Nanotechnology*, **2010**, *21*, 175201 [10.1088/0957-4484/21/17/175201](https://doi.org/10.1088/0957-4484/21/17/175201)

- 300 nm Nickel on a $SiO_2/Si$ wafer
    - CNF
    - $SiO_2$ ~ 290 nm
    - at 0.4 angstrom/s
- Graphene Growth[^Kim2009jan] [^Jo2010apr]
    - Furnace, McEuen Lab, Kyle Dorsey
    - Deposition
        - 900 $^\circ C$, 5 sccm $H_2$, 5 sccm $CH_4$, 100 sccm $Ar$
    - Approx. 3.5 hrs

## Multi-Layer Graphene: Growth{#w100}

![Furnace](figures/mlg_furnace.jpg){width=90%}

## Multi-Layer Graphene: Etch{#w55}

- Copper Etchant ($FeCl_3$): Approx. 25 - 40 mins
- The graphene/Ni/$SiO_2$/Si piece (1 cm x 2 cm) floats on the etchant

![Nickel Etch (first attempt)](figures/mlg_etch_1.jpg){width=55%}

## Multi-Layer Graphene: Etch{#w35}

### Problem:

- Etch from the side and inwards.
- Etch rate depends on 1) piece size, 2) shape of the cut and 3) the "starting point"

![Nickel Etch (multiple break points)](figures/mlg_etch_2.jpg){width=35%}
![Nickel Etch ("etch corner" created)](figures/mlg_etch_3.jpg){width=35%}

## Multi-Layer Graphene: Etch{#w47}

**Solution**: low etchant volume (breaks into 3 large pieces when transferred: inherent stress when etching)  

![Nickel Etch (complete piece)](figures/mlg_etch_4.jpg){width=47%}

## Multi-Layer Graphene: Transfer{#w80}

- Use watch glass to scoop up the whole graphene piece and place into D.I water. (3 times)
- The waveguide are approached from top and "stamp" motion (not perfect)
- Dry with nitrogen gun first and store in glovebox vacuum for 16 - 20 hrs.

![Graphene on polystyrene](figures/mlg_pswg_1.jpg){width=80%}

## Multi-Layer Graphene: Characterization {#w60}

### Conductivity

- Transferred graphene onto a waveguide (without polystyrene): 
    - conductive (from 2 $M\Omega$ to 60 - 40 $\Omega$)

### Thickness

- Profilometry (CCMR): ~ 15 nm (max 20 nm)
- Raman Spectroscopy (CCMR): 488 nm Laser

## Multi-Layer Graphene: Raman Spectroscopy {#w90}

![Raman Spectroscopy of Graphene on Silicon](figures/mlg_raman.png){width=90%}

## Multi-Layer Graphene: Raman Spectroscopy {#w90}

![Raman Spectroscopy of Graphene on Silicon - Standard](figures/mlg_raman_ex.png){width=90%}


## Multi-Layer Graphene: Current and Future  
  
$\checkmark$ Growth  
$\checkmark$ Etch Technique  
$\checkmark$ Transfer on Silicon or waveguide  
$\checkmark$ Transfer on polystyrene  

$\bowtie$ Polystyrene on waveguide surface modification  

$\Box$ Transfer on modified polystyrene/waveguide & characterization  
$\Box$ AFM surface profile (waiting for training)  
$\Box$ Transfer onto sample  
$\Box$ Check spin radical abundance post-transfer  
$\Box$ Transfer Technique Improvements  
$\Box$ Growth options/improvements  

## Multi-Layer Graphene: Surface Modification {#w100}

![General Scheme of Sample Surface](figures/sample_surface.jpg){width=100%}

## Multi-Layer Graphene: Surface Modification {#w35}

![Swab Tip Modification](figures/swab_mod.jpg){width=35%}

$\bigotimes$ **NO**  

- Cleaning with Toluene not sufficient:   
    - Hard to clean throughout (3 times on silicon wafer)
    - Hard to control: multiple facets, often end up on center line
    - Surface profile not ideal
        - If a tiny droplet forms, the edge could go up to 2 $\mu m$

## Multi-Layer Graphene: Surface Modification {#w80}

$\bigotimes$ **NO**  

- "Drop Cast" PVA first and spin coat Polystyrene  
    - Polystyrene was coated on top of PVA

$\bowtie$ Glue Mica on Waveguide with PVA

![Mica glued on waveguide](figures/wg_mica.jpg){width=80%}

# Blender

## Blender: General {#w80}

Open Source 3D Software with API for python scripting  
Used Blender 2.78c (current version 2.8)  
![Blender Interface](figures/Blender_gui.png){width=80%}
 

## Animation: Pipeline {#w47}

Modeling $\implies$ Material/Color $\implies$ Animation $\implies$ Rendering $\implies$ Post Sequence Edit  


## Animation: Modeling {#w47}

Object, Light and Camera

![Blender Model Raw](figures/Model_Raw_1.png){width=50%}
![Blender Model Raw](figures/Model_Raw_2.png){width=50%}

## Animation: Material/Color {#w47}

<br>
![Blender Material Diffuse](figures/Material_1.png){width=50%}
![Blender Material Glossy](figures/Material_2.png){width=50%}

## Animation: Material/Color {#w47}

<br>
![Blender Material Diffuse Rendered](figures/Material_1_render.png){width=50%}
![Blender Material Glossy Rendered](figures/Material_2_render.png){width=50%}

## Animation: Render

Cycles Render: [Path Tracing](https://en.wikipedia.org/wiki/Path_tracing)

<div style="float: left; width: 60%>
![Path Trace Samples](figures/Path_Trace.png){width=50%}
</div>

<div style="float: right; width: 40%; font-size: 90%">
![Blender Render Menu](figures/Render_Menu.png){width=50%}
</div>  


## Animation: MRFM {#w80}
![MRFM Render Wire Frame Example](figures/Render_MRFM_1.png){width=90%}

## Animation: MRFM {#w90}

![MRFM Render Preview](figures/Render_MRFM_2.png){width=90%}

## Animation: Timeline and DopeSheet {#w90}

![Blender Animation Interface](figures/Animation_1.png){width=100%}

## Animation: Timeline and DopeSheet {#w90}

![Blender Animation Interface](figures/Animation_2.png){width=100%}


## Animation: Post Edit {#w90}

![Blender Post Edit](figures/Post_Edit.png){width=105%}

## Blender: Python Scripting

```python

import bpy
import numpy as np

D = bpy.data

def spin_ori(startframe, endframe, frame_steps, xyz_rad_list, obj):
    frame_range = np.arange(startframe, endframe, frame_steps)
    for key_frame in frame_range:
        D.objects[obj].rotation_euler = xyz_rad_list[key_frame]
        D.objects[obj].keyframe_insert(data_path = "rotation_euler", frame = key_frame)

spin_ori(845,900, 1, xyz_rad_spin2, "Spin6")
```

## Blender: AWS {#w100}

[Primary] EC2 CPU: c4.8xlarge   
[AWS Script](aws_blender.html)

![AWS EC2 Interface](figures/AWS_EC2.png){width=100%}

# DoiToBib_Lite 

## DoiToBib_Lite: GUI {#w90}

Python3 + Qt5.9
![DoiToBib_GUI](figures/doitobib_lite_gui.png){width=90%}

# Reference & Acknowledgement

## Reference 

<br>
**Kim2009jan** Kim, K.S. et al. "Large-scale pattern growth of graphene films for stretchable transparent electrodes", *Nature Letter*, **2009**, *457*, 706-710 [10.1038/nature07719](https://doi.org/10.1038/nature07719)  

**Jo2010apr** Jo, G. et al. "Large-scale patterned multi-layer graphene films as transparent conducting electrodes for GaN light-emitting diodes", *Nanotechnology*, **2010**, *21*, 175201 [10.1088/0957-4484/21/17/175201](https://doi.org/10.1088/0957-4484/21/17/175201)

## Acknowledgement

**Prof. John Marohn** for letting me be here  

**Kyle Dorsey**, McEuen Lab at Cornell, for graphene preparation  

**Benjamin Richard**, Hanrath Group at Cornell, for Blender introduction  

**Hoang Long Nguyen, Corinne Issac, Michael Boucher, Ali Tirmzi and Jacelyn Greenwald**, Marohn Group at Cornell, for answering all my endless weird questions  

**Michael Boucher and Ali Tirmzi**, Marohn Group at Cornell, for inspiring me to be a YouTuber  


## Acknowledgement

![](figures/Group_Pic.jpg){width=105%}

