# Harmonic Tremolo for Zoom MultiStomp

A pedal-safe harmonic tremolo effect for Zoom ZDL-compatible pedals. It splits the signal into complementary low and high bands, then modulates the bands in opposite phase for the classic pulsing, phase-shifting tremolo sound.

## Controls

- **Rate** — LFO speed, approximately 0.1–8 Hz.
- **Depth** — intensity of the alternating band modulation; zero is neutral, maximum can silence one band at each LFO extreme.
- **Xover** — low/high crossover, approximately 150–1800 Hz.
- **Mix** — dry/wet blend.

The DSP is written for the Zoom MultiStomp ZDL toolchain and follows its safe-DSP conventions: no math-library calls, runtime divides, dynamic allocation, or writable global state; persistent filter/LFO state lives in the per-instance `ctx[3]` arena. The effect ID is 947 (Delay group), the next available ID identified in the upstream registry when this project was created; check other effect collections before installing alongside third-party ZDLs.

## Build

Requires Python 3 and the TI C6000 compiler. The build script currently expects TI CGT 8.5.0 at `/Applications/ti/ti-cgt-c6000_8.5.0.LTS`; edit `TI_ROOT` in `src/custom/harmonic/build.py` if needed.

```sh
python3 src/custom/harmonic/build.py
```

The resulting `dist/Harmonic.ZDL` can be installed with Zoom Effect Manager. Start with the generated UI-only smoke build (`audio_nop: true`) for a hardware load test, then set it to `false` and rebuild to enable audio processing. Hardware validation is still required before relying on a custom ZDL; back up pedal data first.
