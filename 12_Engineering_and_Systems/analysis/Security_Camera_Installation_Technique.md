# Security Systems — Camera Installation Technique

Detail page for [[12_Engineering_and_Systems/analysis/Security_Systems|Security Systems]]. Sources: Vasily Tarasov (Ucam / Системы видеонаблюдения, CCTV-kit retailer/installer) and Рабочая Молодежь (a real personal DIY project — a woodworking-workshop camera install). [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_Qymq81j2wJ0_tarasov_camera_system_diy_install|Qymq81j2wJ0]]] [source: [[11_Budget_and_Planning/_supporting/knowledge/sources/YT_aD0piOY523I_rabochaya_molodezh_camera_system_diy_simple|aD0piOY523I]]]

## DVR-Based Coax System (Vasily Tarasov / Ucam)

- **⚠️ Screw the HDD into the DVR chassis, don't just set it in place** — HDDs vibrate slightly during operation; an unsecured drive knocks against the housing repeatedly, causing failure over roughly 1-1.5 years.
- **КВК combined CCTV cable**: 3 conductors — two thin power leads (red = "+", black = "-") plus one thick coaxial conductor for video.
- **BNC connector assembly, step by step**: strip the coax's inner conductor to expose ~4mm; thread the outer sleeve onto the cable first (before crimping); insert the center conductor into the BNC pin and tighten the small screw — **⚠️ don't over-torque, it strips/breaks easily**; the braided shield goes under the connector's "alligator clip" tabs, then crimped down to secure it.
- **Multi-format camera jumper-pin behavior**: this camera model supports 4 signal formats via small jumper wires; leaving them unconnected defaults to HD (the source's preferred default). **⚠️ Insulate/tape these exposed jumper wires** — water bridging the contacts can change the camera's signal format unexpectedly.
- **Prefer WAGO lever connectors over plain twisted joints for all power splicing** — a twisted-only joint is a real, checkable cause of intermittent signal/power loss; WAGO connections don't loosen or short over time.
- **Scaling beyond the kit's included connectors**: simply twist two additional wire ends together and insert into one more port of the same WAGO connector — described as equally secure, not a compromise. System scales to **up to 16 cameras** this way.
- **Assembly order**: HDD into DVR → BNC prep → power-terminal prep → camera-side connections → power-supply-side connections → confirm image on monitor/DVR before moving to the next camera.

## SD-Card-Per-Camera System, No DVR (Рабочая Молодежь)

Real personal project (6-camera install in a new woodworking workshop, ~55m², 4 exterior + 2 interior). **A real case with reasoning, not just an outcome** — genuinely favored per this vault's value-filter criteria.

- **Chose a fully Russian-made system after a bad prior experience with cheap China-sourced cameras** — reasoning not fully detailed on camera, recorded as a real practitioner judgment call rather than a substantiated technical claim.
- **⚠️ SD-card-per-camera architecture as an alternative to a central DVR**: each camera is its own self-contained recorder (64GB SD card used, judged more than sufficient), while still groupable/viewable together in one app. **Detection-based recording (not continuous)** conserves storage and keeps archive browsing practical — you see exactly when motion occurred instead of scrubbing continuous footage.
- **PoE switch vs. separate 12V power per camera — a real cost/convenience tradeoff**: PoE (≥6 ports for 6 cameras here) means power and data travel over one cable per camera. Cheaper non-PoE switch alternative requires a local 12V supply near each camera's mounting point — pick based on whether power is already available at each location.
- **⚠️ Router/switch mains supply must be grounded**; the source used a dedicated RCD/differential breaker on that circuit as extra protection.
- **⚠️ Real gotcha**: verify the router's power-supply plug physically fits the installed outlet *before* finalizing the mounting location — the source had to redo an outlet after discovering a mismatch.
- **Suspended/drop ceiling used to conceal networking infrastructure from workshop dust** — equipment simply rests on an extra ceiling tile inset into the grid, no dedicated shelf needed. Directly relevant technique for any dusty utility/workshop space.
- **Structured cabling**: copper conductor is the professional-installer-recommended standard vs. copper-clad aluminum, though the source used copper-clad aluminum with no observed problems — flagged explicitly as the reader's own risk tradeoff, not a settled recommendation.
- **⚠️ Cable slack/service-loop rule**: leave extra cable length at each run to allow re-crimping or future repair — zero slack pulled taut is a real mistake to avoid.
- **RJ-45 crimping (T568B order)**: white-orange, orange, white-green, blue, white-blue, green, white-brown, brown; strip ~2cm, trim to ~1cm, clip facing down, crimp. **⚠️ Use different-colored connector boots per camera run** — a simple labeling technique for later maintenance. **Test every crimped run with a cable tester** — all-green LEDs confirm correct pinout.
- **App feature highlighted as genuinely useful**: motion-triggered short video clips automatically forwarded to Telegram, alongside local SD-card and cloud storage — a real redundancy/notification pattern, plus configurable sensitivity/zone/object-size detection settings.
- **⚠️ Real time-cost data point**: full 6-camera install (cable runs, drilling exterior walls at an angle for water runoff, crimping, mounting, app setup) took **one full working day** — evidence the process is approachable for a motivated DIYer, not requiring professional installation.

## Assumptions / Uncertainties

Neither source states a specific city/region (Рабочая Молодежь confirms only that the cloud data center is Russia-based, a company-infrastructure fact, not a pricing location). Both `single-account`, medium promotional ratio (Tarasov: end-video kit sales link; Рабочая Молодежь: affiliate links in the description, but genuine first-hand project narrative). The ~90 RUB junction-box price point (Рабочая Молодежь, 2023) is too small a figure to be load-bearing and isn't currency-converted here — see [[12_Engineering_and_Systems/analysis/Security_Systems|Security Systems]] for the security reasoning behind that choice.
