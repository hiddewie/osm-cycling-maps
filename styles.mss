// Font
@font : 'DejaVu Sans Book';
@font-bold : 'DejaVu Sans Bold';

// Colors
@forest : rgb(222, 245, 198);

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
    polygon-fill: rgb(201, 180, 133);
  }

  [fclass='military'] {
    polygon-fill: rgba(255, 51, 51, 0.6);
    line-color: rgb(255, 0, 0);
  }
}

#country {
  ::border {
    line-color: rgba(0, 219, 68, 0.45);
    line-width: 9.0;
  }

  line-color: rgba(0, 74, 24, 0.8);
  line-width: 1.0;
  line-dasharray: 10, 4;
}

#waterways {
  line-color: rgb(53, 134, 212);
}

#water {
  polygon-fill: rgb(123, 179, 232);
  line-width: 1.0;
  line-color: rgb(53, 134, 212);
}

#springs {
  marker-width: 3;
  marker-fill: rgb(123, 179, 232);
  marker-line-color: rgb(53, 134, 212);
  marker-line-width: 1.0;
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

// TODO group symbolizer?
//   see https://github.com/mapnik/mapnik/wiki/GroupSymbolizer

#transport {
  ::background {
    marker-file: 'data/icons/maki/circle-11.svg';
    marker-transform: 'scale(1.2, 1.2)';
    marker-fill: rgba(250, 250, 250, 0.8);
    marker-allow-overlap: false;
    marker-ignore-placement: true;
  }

  marker-transform: 'scale(0.68, 0.68)';
  marker-fill: purple;
  marker-allow-overlap: false;
  marker-ignore-placement: true;

  [fclass='railway_station'],
  [fclass='railway_halt'] {
    marker-file: 'data/icons/maki/rail-11.svg';
  }
  [fclass='ferry_terminal'] {
    marker-file: 'data/icons/maki/ferry-11.svg';
  }
  [fclass='airfield'] {
    marker-file: 'data/icons/maki/airfield-11.svg';
  }
  [fclass='airport'] {
    marker-file: 'data/icons/maki/airport-11.svg';
  }
}

#power-line {
  line-color: rgb(150, 150, 150);
  line-width: 1.0;
}

#power-pole {
  marker-file: 'data/icons/maki/square-11.svg';
  marker-width: 2;
  marker-fill: rgb(150, 150, 150);
  marker-allow-overlap: true;
  marker-ignore-placement: true;
}

#poi {
  ::background {
    marker-file: 'data/icons/maki/circle-11.svg';
    marker-width: 12;
    marker-fill: rgba(250, 250, 250, 0.8);
    marker-allow-overlap: false;
    marker-ignore-placement: true;
  }

  marker-width: 10;
  marker-fill: purple;
  marker-allow-overlap: false;
  marker-ignore-placement: true;

  [fclass='camp_site'] {
    marker-file: 'data/icons/maki/campsite-11.svg';
  }
  [fclass='hospital'] {
    marker-file: 'data/icons/maki/hospital-11.svg';
  }
  [fclass='swimming_pool'] {
    marker-file: 'data/icons/maki/swimming-11.svg';
  }
  [fclass='caravan_site'] {
    marker-file: 'data/icons/svg/caravan_site.svg';
  }
  [fclass='supermarket'] {
    marker-width: 8;
    marker-file: 'data/icons/maki/shop-11.svg';
  }
  [fclass='bicycle_shop'] {
    marker-file: 'data/icons/maki/bicycle-11.svg';
  }
  [fclass='castle'],
  [fclass='fort'] {
    marker-file: 'data/icons/maki/castle-11.svg';
  }
  [fclass='ruins'] {
    marker-file: 'data/icons/svg/ruins.svg';
  }
  [fclass='tower_comms'] {
    marker-file: 'data/icons/maki/communications-tower-11.svg';
  }
  [fclass='tower_observation'] {
    marker-file: 'data/icons/maki/viewpoint-11.svg';
  }
  [fclass='tower'] {
    marker-width: 6;
    marker-file: 'data/icons/svg/tower.svg';
  }
  [fclass='lighthouse'] {
    marker-file: 'data/icons/maki/lighthouse-11.svg';
  }
}

#religious {
  ::background {
    marker-file: 'data/icons/maki/circle-11.svg';
    marker-width: 12;
    marker-fill: rgba(250, 250, 250, 0.8);
    marker-allow-overlap: false;
    marker-ignore-placement: true;
  }

  marker-width: 10;
  marker-fill: purple;
  marker-allow-overlap: false;
  marker-ignore-placement: true;

  [fclass='christian'],
  [fclass='christian_anglican'],
  [fclass='christian_catholic'],
  [fclass='christian_evangelical'],
  [fclass='christian_lutheran'],
  [fclass='christian_methodist'],
  [fclass='christian_orthodox'],
  [fclass='christian_protestant'],
  [fclass='christian_babtist'],
  [fclass='christian_mormon'] {
    marker-width: 6;
    marker-file: 'data/icons/maki/religious-christian-11.svg';
  }
  [fclass='jewish'] {
    marker-file: 'data/icons/maki/religious-jewish-11.svg';
  }
  [fclass='muslim'],
  [fclass='muslim_sunni'],
  [fclass='muslim_shia'] {
    marker-file: 'data/icons/maki/religious-muslim-11.svg';
  }
  [fclass='buddhist'] {
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