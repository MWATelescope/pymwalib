# pymwalib Examples

The `view_fits.py` example provides basic plotting functionality.

Command line usage:

```bash
usage: view_fits.py [-h] -m METAFITS [-t1 TIMESTEP1] [-t2 TIMESTEP2] [-a1 ANT1] [-a2 ANT2] [-c1 CHANNEL1] [-c2 CHANNEL2] [-a] [-p] [-p2] [-g] [-g2] [-gp GRIDPOL] [-ph] [-ph1] -o MODE [-dr] [-dp] filename

positional arguments:
  filename              fits filename

optional arguments:
  -h, --help            show this help message and exit
  -m METAFITS, --metafits METAFITS
                        Path to the metafits file.
  -t1 TIMESTEP1, --timestep1 TIMESTEP1
                        timestep start (1 based index)
  -t2 TIMESTEP2, --timestep2 TIMESTEP2
                        timestep end (defaults to last index)
  -a1 ANT1, --ant1 ANT1
                        antenna (start)
  -a2 ANT2, --ant2 ANT2
                        antenna (end)
  -c1 CHANNEL1, --channel1 CHANNEL1
                        fine channel number (start)
  -c2 CHANNEL2, --channel2 CHANNEL2
                        fine channel number (end)
  -a, --autosonly       Only output the auto correlations
  -p, --ppdplot         Create a ppd plot
  -p2, --ppdplot2       Create a ppd plot that does not sum across all baselines. ie it plots all baselines
  -g, --gridplot        Create a grid / baseline plot
  -g2, --gridplot2      Create a grid / baseline plot but show a single pol (XX,XY,YX,YY) for each tile. Use gridpol to specify
  -gp GRIDPOL, --gridpol GRIDPOL
                        If gridplot2 used, use this to specify the pol. Default is 'XX'
  -ph, --phaseplot_all  Will do a phase plot for all baselines for given antennas and timesteps
  -ph1, --phaseplot_one
                        Will do a phase plot for given baseline and timesteps
  -o MODE, --mode MODE  How to interpret a1 and a2: RANGE or BASELINE
  -dr, --dump-raw       Dump the raw data
  -dp, --dump-plot      Dump the plot data
```

Example of plotting phase vs frequency for antennas 100->109 and timesteps 2-8:

```bash
python examples/view_fits.py -m /data/1339927336.metafits /data/1339927336_20220622100158_ch121_000.fits -a1 100 -a2 109 -t1 2 -t2 8 --mode=RANGE -ph
```

Phase vs frequency for multiple timesteps results in the plot adding more points as it works through each timestep. The values are not integrated across timesteps.

Example of plotting power vs frequency for the baseline 0 v 0 and timesteps 2-8:

```bash
python examples/view_fits.py -m /data/1339927336.metafits /data/1339927336_20220622100158_ch121_000.fits -a1 0 -a2 0 -t1 2 -t2 8 --mode=BASELINE -p
```
