# Gas Giant Infographics

This Python script generates infographic posters that visualise data about the outer planets in our solar system.
You can find some pre-generated diagrams [here](https://github.com/codebox/solar-system-moons/tree/master/pregenerated).

<img src="https://codebox.net/assets/images/gas-giants/jupiter_small.png" alt="Jupiter Infographic" width="400"/><img src="https://codebox.net/assets/images/gas-giants/saturn_small.png" alt="Saturn Infographic" width="400"/><br>
<img src="https://codebox.net/assets/images/gas-giants/uranus_small.png" alt="Uranus Infographic" width="400"/><img src="https://codebox.net/assets/images/gas-giants/neptune_small.png" alt="Neptune Infographic" width="400"/>

The script has been written using Python 3, and has no external dependencies. To generate the diagrams just run the `go.sh` script from the root of the project:

    ./go.sh

The left-most section of each diagram shows the relative sizes of the orbits of each planet's moons:

<img src="https://codebox.net/assets/images/gas-giants/orbit_detail.png" alt="Orbit Detail" width="400"/>

The right-most section shows the relative sizes of the moons themselves, with the radius of each shown in kilometers.
At the top of this section the diagram shows a small part of the parent planet drawn at the same scale:

<img src="https://codebox.net/assets/images/gas-giants/radius_detail.png" alt="Radius Detail" width="400"/>

Each planet's ring system is illustrated in the top center section, with the planet's disc shown for scale:

<img src="https://codebox.net/assets/images/gas-giants/rings_detail.png" alt="Ring System Detail" width="600"/>

The orbital paths of all the moons are shown in the center-right section, illustrating the size, shape and orientation of each:

<img src="https://codebox.net/assets/images/gas-giants/eccentricity_detail.png" alt="Eccentricity Detail" width="600"/>

The rotational axis of each moon is shown in the bottom-center section:

<img src="https://codebox.net/assets/images/gas-giants/rotation_detail.png" alt="Rotation Detail" width="600"/>
