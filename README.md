# Gas Giant Infographics

This Python script generates infographic posters that visualise data about the outer planets in our solar system.
You can find some pre-generated diagrams [here](https://github.com/codebox/solar-system-moons/tree/master/pregenerated).

![Jupiter Infographic](//codebox.net/assets/images/gas-giants/jupiter_small.png)
![Saturn Infographic](//codebox.net/assets/images/gas-giants/saturn_small.png)
![Uranus Infographic](//codebox.net/assets/images/gas-giants/uranus_small.png)
![Neptune Infographic](//codebox.net/assets/images/gas-giants/neptune_small.png)

The script has been written using Python 3, and has no external dependencies. To generate the diagrams just run the `go.sh` script from the root of the project:

    ./go.sh

The left-most section of each diagram shows the relative sizes of the orbits of each planet's moons:

![Orbit Detail](//codebox.net/assets/images/gas-giants/orbit_detail.png)

The right-most section shows the relative sizes of the moons themselves, with the radius of each shown in kilometers.
At the top of this section the diagram shows a small part of the parent planet drawn at the same scale:

![Radius Detail](//codebox.net/assets/images/gas-giants/radius_detail.png)

Each planet's ring system is illustrated in the top center section, with the planet's disc shown for scale:

![Ring System Details](//codebox.net/assets/images/gas-giants/rings_detail.png)

The orbital paths of all the moons are shown in the center-right section, illustrating the size, shape and orientation of each:

![Eccentricity Detail](//codebox.net/assets/images/gas-giants/eccentricity_detail.png)

The rotational axis of each moon is shown in the bottom-center section:

![Rotation Detail](//codebox.net/assets/images/gas-giants/rotation_detail.png)
