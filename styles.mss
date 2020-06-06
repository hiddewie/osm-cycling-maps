// Font
@font: 'DejaVu Sans Book';
@font-bold: 'DejaVu Sans Bold';
@font-italic: 'DejaVu Sans Oblique';
@font-serif-italic: 'DejaVu Serif Italic';

// Colors
@forest: rgb(222, 245, 198);

#landuse-background {
  [fclass='forest'] {
    polygon-fill: @forest;
  }
}

#shade {
  raster-scaling: bilinear;
  raster-comp-op: multiply;
  raster-opacity: 1.0;
}

#contours {
  [boundary='no'] {
    line-color: rgba(145, 132, 83, 0.4);
    line-width: 0.5;
  }

  [boundary='yes'] {
    line-color: rgba(145, 132, 83, 0.6);
    line-width: 1.0;
  }
}

#landuse-foreground {
  [fclass='residential'] {
    polygon-fill: rgb(205, 202, 175);
  }

  [fclass='military'] {
    polygon-pattern-file: url('data/background/military.svg');
    polygon-pattern-comp-op: multiply;
    polygon-pattern-alignment: global;
    line-color: rgb(255, 0, 0);
  }
}

@admin-background: rgb(0, 219, 68);
@admin-boundaries: rgb(0, 74, 24);

#administrative-boundaries {
  ::firstline {
    background/line-join: round;
    background/line-color: white;
    background/line-width: 7;
  }

  ::wideline {
    background/line-join: round;
    background/line-color: white;
    background/line-width: 4;

    opacity: 0.2;
    line-color: @admin-background;
    line-join: bevel;
    line-width: 4;

    [admin_level < 4] {
      background/line-width: 7;
      line-width: 7;
    }
  }

  ::narrowline {
    background/line-join: round;
    background/line-color: white;
    background/line-width: 1;

    opacity: 0.6;
    thin/line-color: @admin-boundaries;
    thin/line-width: 1;
    thin/line-dasharray: 12,3,2,3,2,3;

    [admin_level >= 4] {
      thin/line-dasharray: 12,10;
    }
  }

  ::firstline,
  ::wideline,
  ::narrowline {
    comp-op: darken;
  }
}

#cycling-network {
  opacity: 0.6;
  line-color: rgb(255, 210, 80);
  line-width: 7.0;
  line-cap: round;
}

#waterways {
  line-color: rgb(53, 134, 212);
}

#water {
  polygon-fill: rgb(123, 179, 232);
  line-width: 0.5;
  line-color: rgb(123, 179, 232);
}

#ferry {
  line-width: 1.0;
  line-color: rgb(20, 55, 90);
  line-dasharray: 4, 3;
}

#springs {
  marker-width: 3;
  marker-fill: rgb(123, 179, 232);
  marker-line-color: rgb(53, 134, 212);
  marker-line-width: 1.0;
}

#aeroway {
  line-color: @highway;
  line-cap: square;
  line-width: 5;
}

#railways {
  line-color: black;
  line-width: 1.5;
  line-cap: square;

  overlay/line-color: white;
  overlay/line-width: 1;
  overlay/line-cap: square;

  dash/line-color: black;
  dash/line-width: 1;
  dash/line-dasharray: 5, 5;
  dash/line-cap: square;
}

@track: rgb(105, 105, 105);
@cycle: rgb(176,58,240);
@cycle-border: white;
@unclassified: white;
@unclassified-border: rgb(82, 82, 82);
@tertiary: @unclassified;
@tertiary-border: @unclassified-border;
@secondary: rgb(232, 232, 16);
@secondary-border: rgb(99, 99, 6);
@primary: rgb(219, 143, 35);
@primary-border: rgb(168, 109, 25);
@trunk: rgb(158, 158, 158);
@trunk-border: white;
@highway: rgb(120, 120, 120);
@highway-border: white;
@bridge: white;
@bridge-border: black;

#roads::track {
  [fclass='track'],
  [fclass='track_grade1'],
  [fclass='track_grade2'],
  [fclass='track_grade3'],
  [fclass='track_grade4'],
  [fclass='track_grade5'] {
    line-width: 1.0;
    line-color: @track;

    [fclass='track_grade3'],
    [fclass='track_grade4'],
    [fclass='track_grade5'] {
      line-cap: butt;
      line-dasharray: 4, 3;
    }
  }
}
#roads::border {
  [fclass='unclassified'],
  [fclass='residential'] {
    line-width: 2.0;
    line-color: @unclassified-border;
  }

  [fclass='tertiary'] {
    line-width: 3.0;
    line-color: @tertiary-border;
  }

  [fclass='secondary'],
  [fclass='secondary_link'] {
    line-width: 3.0;
    line-color: @secondary-border;
  }

  [fclass='cycleway'] {
    line-width: 2.0;
    line-color: @cycle-border;
  }

  [fclass='primary'],
  [fclass='primary_link'] {
    line-width: 3.0;
    line-color: @primary-border;
  }

  [fclass='trunk'],
  [fclass='trunk_link'] {
    line-width: 3.0;
    line-color: @trunk-border;
  }

  [fclass='motorway'],
  [fclass='motorway_link'] {
    line-width: 3.0;
    line-color: @highway-border;
  }
}

#roads::fill {
  [fclass='secondary_link'] {
    line-width: 2.0;
    line-color: @secondary;
  }

  [fclass='primary_link'] {
    line-width: 2.0;
    line-color: @primary;
  }

  [fclass='trunk_link'] {
    line-width: 2.0;
    line-color: @trunk;
  }

  [fclass='motorway_link'] {
    line-width: 2.0;
    line-color: @highway;
  }

  [fclass='unclassified'],
  [fclass='residential'] {
    line-width: 0.5;
    line-color: @unclassified;
  }

  [fclass='tertiary'] {
    line-width: 2.0;
    line-color: @tertiary;
  }

  [fclass='secondary'] {
    line-width: 2.0;
    line-color: @secondary;
  }

  [fclass='cycleway'] {
    line-width: 1.0;
    line-color: @cycle;
  }

  [fclass='primary'] {
    line-width: 2.0;
    line-color: @primary;
  }

  [fclass='trunk'] {
    line-width: 2.0;
    line-color: @trunk;
  }

  [fclass='motorway'] {
    line-width: 2.0;
    line-color: @highway;
  }
}

#roads::bridge {
  [bridge='T'] {
    [fclass='secondary'],
    [fclass='secondary_link'],
    [fclass='primary'],
    [fclass='primary_link'],
    [fclass='trunk'],
    [fclass='trunk_link'],
    [fclass='motorway'],
    [fclass='motorway_link'] {
      ::bridge-border {
        line-color: @bridge-border;
        line-width: 3.0;
        // TODO round?
        line-cap: butt;
      }

      line-color: @bridge;
      line-width: 1.0;
      line-cap: butt;
    }

    [fclass='secondary_link'] {
      line-width: 2.0;
      line-color: @secondary;
    }
    [fclass='primary_link'] {
      line-width: 2.0;
      line-color: @primary;
    }
    [fclass='trunk_link'] {
      line-width: 2.0;
      line-color: @trunk;
    }
    [fclass='motorway_link'] {
      line-width: 2.0;
      line-color: @highway;
    }

    [fclass='tertiary'] {
      line-width: 2.0;
      line-color: @tertiary;
    }
    [fclass='secondary']  {
      line-width: 2.0;
      line-color: @secondary;
    }
    [fclass='cycleway'] {
      line-width: 1.0;
      line-color: @cycle;
    }
    [fclass='primary'] {
      line-width: 2.0;
      line-color: @primary;
    }
    [fclass='trunk'] {
      line-width: 2.0;
      line-color: @trunk;
    }
    [fclass='motorway'] {
      line-width: 2.0;
      line-color: @highway;
    }
  }
}

#cycling-nodes {
  marker-width: 3;
  marker-fill: rgb(255, 210, 80);
  marker-line-color: black;
  marker-line-width: 0.5;
}

#transport {
  background/marker-width: 10;
  background/marker-fill: purple;
  background/marker-allow-overlap: false;
  background/marker-ignore-placement: true;
  background/marker-line-color: white;
  background/marker-line-width: 2.0;

  marker-width: 10;
  marker-fill: purple;
  marker-allow-overlap: false;
  marker-ignore-placement: true;

  [fclass='railway_station'],
  [fclass='railway_halt'] {
    background/marker-width: 7;
    background/marker-file: 'data/icons/maki/rail-11.svg';
    marker-width: 7;
    marker-file: 'data/icons/maki/rail-11.svg';
  }
  [fclass='ferry_terminal'] {
    background/marker-file: 'data/icons/maki/ferry-11.svg';
    marker-file: 'data/icons/maki/ferry-11.svg';
  }
  [fclass='airfield'] {
    background/marker-file: 'data/icons/maki/airfield-11.svg';
    marker-file: 'data/icons/maki/airfield-11.svg';
  }
  [fclass='airport'] {
    background/marker-file: 'data/icons/maki/airport-11.svg';
    marker-file: 'data/icons/maki/airport-11.svg';
  }
}

#aerodrome {
  background/marker-width: 10;
  background/marker-fill: purple;
  background/marker-allow-overlap: false;
  background/marker-ignore-placement: true;
  background/marker-line-color: white;
  background/marker-line-width: 2.0;

  marker-width: 10;
  marker-fill: purple;
  marker-allow-overlap: false;
  marker-ignore-placement: true;

  background/marker-file: 'data/icons/maki/airport-11.svg';
  marker-file: 'data/icons/maki/airport-11.svg';
}

#power-line {
  line-color: rgb(150, 150, 150);
  line-width: 1.0;
}

#power-pole {
  marker-file: 'data/icons/maki/square-11.svg';
  marker-width: 2;
  marker-fill: rgb(150, 150, 150);
  marker-allow-overlap: false;
  marker-ignore-placement: true;
}

#poi {
  background/marker-width: 10;
  background/marker-fill: purple;
  background/marker-allow-overlap: false;
  background/marker-ignore-placement: true;
  background/marker-line-color: white;
  background/marker-line-width: 2.0;

  marker-width: 10;
  marker-fill: purple;
  marker-allow-overlap: false;
  marker-ignore-placement: true;

  [fclass='camp_site'] {
    background/marker-file: 'data/icons/maki/campsite-11.svg';
    marker-file: 'data/icons/maki/campsite-11.svg';
  }
  [fclass='hospital'] {
    background/marker-file: 'data/icons/maki/hospital-11.svg';
    marker-file: 'data/icons/maki/hospital-11.svg';
  }
  [fclass='swimming_pool'] {
    background/marker-file: 'data/icons/maki/swimming-11.svg';
    marker-file: 'data/icons/maki/swimming-11.svg';
  }
  [fclass='caravan_site'] {
    background/marker-file: 'data/icons/svg/caravan_site.svg';
    marker-file: 'data/icons/svg/caravan_site.svg';
  }
  [fclass='supermarket'] {
    background/marker-width: 8;
    background/marker-file: 'data/icons/maki/shop-11.svg';
    marker-width: 8;
    marker-file: 'data/icons/maki/shop-11.svg';
  }
  [fclass='bicycle_shop'] {
    background/marker-file: 'data/icons/maki/bicycle-11.svg';
    marker-file: 'data/icons/maki/bicycle-11.svg';
  }
  [fclass='castle'],
  [fclass='fort'] {
    background/marker-file: 'data/icons/maki/castle-11.svg';
    marker-file: 'data/icons/maki/castle-11.svg';
  }
  [fclass='ruins'] {
    background/marker-file: 'data/icons/svg/ruins.svg';
    marker-file: 'data/icons/svg/ruins.svg';
  }
  [fclass='tower_comms'] {
    background/marker-file: 'data/icons/maki/communications-tower-11.svg';
    marker-file: 'data/icons/maki/communications-tower-11.svg';
  }
  [fclass='tower_observation'] {
    background/marker-file: 'data/icons/maki/viewpoint-11.svg';
    marker-file: 'data/icons/maki/viewpoint-11.svg';
  }
  [fclass='tower'] {
    background/marker-width: 6;
    background/marker-file: 'data/icons/svg/tower.svg';
    marker-width: 6;
    marker-file: 'data/icons/svg/tower.svg';
  }
  [fclass='lighthouse'] {
    background/marker-file: 'data/icons/maki/lighthouse-11.svg';
    marker-file: 'data/icons/maki/lighthouse-11.svg';
  }
}

#religious {
  background/marker-width: 10;
  background/marker-fill: purple;
  background/marker-allow-overlap: false;
  background/marker-ignore-placement: true;
  background/marker-line-color: white;
  background/marker-line-width: 2.0;
  background/marker-file: 'data/icons/openstreetmap/place_of_worship.svg';

  marker-width: 10;
  marker-fill: purple;
  marker-allow-overlap: false;
  marker-ignore-placement: true;
  marker-file: 'data/icons/openstreetmap/place_of_worship.svg';

  [religion='christian'] {
    background/marker-width: 6;
    background/marker-file: 'data/icons/maki/religious-christian-11.svg';
    marker-width: 6;
    marker-file: 'data/icons/maki/religious-christian-11.svg';
  }
  [religion='jewish'] {
    background/marker-file: 'data/icons/maki/religious-jewish-11.svg';
    marker-file: 'data/icons/maki/religious-jewish-11.svg';
  }
  [religion='muslim'] {
    background/marker-file: 'data/icons/maki/religious-muslim-11.svg';
    marker-file: 'data/icons/maki/religious-muslim-11.svg';
  }
  [religion='buddhist'] {
    background/marker-file: 'data/icons/maki/religious-buddhist-11.svg';
    marker-file: 'data/icons/maki/religious-buddhist-11.svg';
  }
}

#places {
  text-name: '[name]';
  text-size: 7;
  text-face-name: @font;
  text-fill: black;
  text-halo-radius: 1.0;
  text-halo-fill: rgba(255, 255, 220, 0.7);
  text-placement-type: simple;
  text-placements: 'S,N,E,W';
  text-dx: 10;
  text-dy: 8;

  [fclass='national_capital'],
  [fclass='city'] {
    text-transform: uppercase;
  }

  [fclass='national_capital'],
  [fclass='city'],
  [fclass='town'] {
    text-face-name: @font-bold;
  }

  [fclass='national_capital'] {
    text-size: 18;
  }
  [fclass='city'] {
    text-size: 14;
  }
  [fclass='town'] {
    text-size: 12;
  }
  [fclass='village'] {
    text-size: 10;
  }
}

#cycling-nodes-labels {
  text-name: '[ref]';
  text-size: 7;
  text-face-name: @font-serif-italic;
  text-fill: black;
  text-halo-radius: 1.0;
  text-halo-fill: rgba(255, 210, 80, 0.7);
  text-placement-type: simple;
  text-placements: 'S,N,E,W';
  text-dx: 5;
  text-dy: 4;
}

#roads::labels {
  [fclass='tertiay'],
  [fclass='secondary'],
  [fclass='primary'],
  [fclass='trunk'],
  [fclass='motorway'] {
    text-name: '[ref]';
    text-size: 8;
    text-face-name: @font;
    text-fill: white;
    text-halo-radius: 1.0;
    text-min-path-length: 70;
    text-min-distance: 100;
    text-spacing: 100;
    text-placement: line;

    [fclass='tertiary'] {
      text-size: 7;
    }

    [fclass='tertiary'] {
      text-halo-fill: rgb(82, 82, 82);
    }
    [fclass='secondary'] {
      text-halo-fill: rgb(99, 99, 6);
    }
    [fclass='primary'] {
      text-halo-fill: rgb(168, 109, 25);
    }
    [fclass='trunk'] {
      text-halo-fill: rgb(115, 35, 17);
    }
    [fclass='motorway'] {
      text-halo-fill: black;
    }
  }
}

#contours {
  [boundary='yes']::label {
    text-name: '[height]';
    text-fill: rgb(145, 132, 83);
    text-face-name: @font;
    text-size: 6;
    text-halo-fill: white;
    text-halo-radius: 1.0;
    text-placement: line;
    text-min-path-length: 50;
  }
}