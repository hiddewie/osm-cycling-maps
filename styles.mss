// Font
@font: 'DejaVu Sans Book';
@font-bold: 'DejaVu Sans Bold';
@font-italic: 'DejaVu Sans Oblique';
@font-serif-italic: 'DejaVu Serif Italic';

// Colors
@forest: rgb(222, 245, 198);

#landuse-background {
  [type = 'forest'] {
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
  [type = 'residential'] {
    polygon-fill: rgb(222, 220, 201);
  }

  [type = 'military'] {
    polygon-pattern-file: url('data/background/military.svg');
    polygon-pattern-comp-op: multiply;
    polygon-pattern-alignment: global;
    line-color: rgb(255, 51, 51);
    line-opacity: 0.335;
    line-width: 1.5;
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
  line-color: rgb(27, 74, 123);
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
  [type = 'track'] {
    line-width: 1.0;
    line-color: @track;

    [tracktype = 'grade3'],
    [tracktype = 'grade4'],
    [tracktype = 'grade5'] {
      line-cap: butt;
      line-dasharray: 4, 3;
    }
  }

  [type = 'path'][bicycle = 'T'] {
    line-color: @cycle;
    line-dasharray: 4, 3;
  }
}
#roads::border {
  [type = 'unclassified'],
  [type = 'service'],
  [type = 'residential'], {
    line-width: 2.0;
    line-color: @unclassified-border;
  }

  [type = 'tertiary'] {
    line-width: 3.0;
    line-color: @tertiary-border;
  }

  [type = 'secondary'],
  [type = 'secondary_link'] {
    line-width: 3.0;
    line-color: @secondary-border;
  }

  [type = 'cycleway'] {
    line-width: 2.0;
    line-color: @cycle-border;
  }

  [type = 'primary'],
  [type = 'primary_link'] {
    line-width: 3.0;
    line-color: @primary-border;
  }

  [type = 'trunk'],
  [type = 'trunk_link'] {
    line-width: 3.0;
    line-color: @trunk-border;
  }

  [type = 'motorway'],
  [type = 'motorway_link'] {
    line-width: 3.0;
    line-color: @highway-border;
  }
}

#roads::fill {
  [type = 'secondary_link'] {
    line-width: 2.0;
    line-color: @secondary;
  }

  [type = 'primary_link'] {
    line-width: 2.0;
    line-color: @primary;
  }

  [type = 'trunk_link'] {
    line-width: 2.0;
    line-color: @trunk;
  }

  [type = 'motorway_link'] {
    line-width: 2.0;
    line-color: @highway;
  }
  [type = 'unclassified'],
  [type = 'service'],
  [type = 'residential'] {
    line-width: 0.5;
    line-color: @unclassified;
  }

  [type = 'tertiary'] {
    line-width: 2.0;
    line-color: @tertiary;
  }

  [type = 'secondary'] {
    line-width: 2.0;
    line-color: @secondary;
  }

  [type = 'cycleway'] {
    line-width: 1.0;
    line-color: @cycle;
  }

  [type = 'primary'] {
    line-width: 2.0;
    line-color: @primary;
  }

  [type = 'trunk'] {
    line-width: 2.0;
    line-color: @trunk;
  }

  [type = 'motorway'] {
    line-width: 2.0;
    line-color: @highway;
  }
}

#roads::bridge {
  [bridge='T'] {
    [type = 'secondary'],
    [type = 'secondary_link'],
    [type = 'primary'],
    [type = 'primary_link'],
    [type = 'trunk'],
    [type = 'trunk_link'],
    [type = 'motorway'],
    [type = 'motorway_link'] {
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

    [type = 'secondary_link'] {
      line-width: 2.0;
      line-color: @secondary;
    }
    [type = 'primary_link'] {
      line-width: 2.0;
      line-color: @primary;
    }
    [type = 'trunk_link'] {
      line-width: 2.0;
      line-color: @trunk;
    }
    [type = 'motorway_link'] {
      line-width: 2.0;
      line-color: @highway;
    }

    [type = 'tertiary'] {
      line-width: 2.0;
      line-color: @tertiary;
    }
    [type = 'secondary']  {
      line-width: 2.0;
      line-color: @secondary;
    }
    [type = 'cycleway'] {
      line-width: 1.0;
      line-color: @cycle;
    }
    [type = 'primary'] {
      line-width: 2.0;
      line-color: @primary;
    }
    [type = 'trunk'] {
      line-width: 2.0;
      line-color: @trunk;
    }
    [type = 'motorway'] {
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
  background/marker-ignore-placement: true;
  background/marker-line-color: white;
  background/marker-line-width: 2.0;

  marker-width: 10;
  marker-fill: purple;

  [type = 'train_station'] {
    background/marker-width: 6;
    background/marker-file: 'data/icons/maki/square-11.svg';
    marker-width: 6;
    marker-file: 'data/icons/maki/square-11.svg';
  }
  [type = 'aerodrome'] {
    background/marker-file: 'data/icons/maki/airport-11.svg';
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
  marker-ignore-placement: true;
}

#poi {
  background/marker-width: 10;
  background/marker-fill: purple;
  background/marker-ignore-placement: true;
  background/marker-line-color: white;
  background/marker-line-width: 2.0;

  [type = 'camp_site'],
  [type = 'caravan_site'],
  [type = 'ruins'] {
    background/marker-line-width: 50.0;
  }

  marker-width: 10;
  marker-fill: purple;

  [type = 'camp_site'] {
    background/marker-width: 9;
    background/marker-file: 'data/icons/svg/camp_site.svg';
    marker-width: 9;
    marker-file: 'data/icons/svg/camp_site.svg';
  }
  [type = 'hospital'] {
    background/marker-file: 'data/icons/maki/hospital-11.svg';
    marker-file: 'data/icons/maki/hospital-11.svg';
  }
  [type = 'caravan_site'] {
    background/marker-file: 'data/icons/svg/caravan_site.svg';
    marker-file: 'data/icons/svg/caravan_site.svg';
  }
  [type = 'supermarket'] {
    background/marker-width: 7;
    background/marker-file: 'data/icons/openstreetmap/shop2.svg';
    marker-width: 7;
    marker-file: 'data/icons/openstreetmap/shop2.svg';
  }
  [type = 'bicycle_shop'] {
    background/marker-width: 9;
    background/marker-file: 'data/icons/maki/bicycle-11.svg';
    marker-width: 9;
    marker-file: 'data/icons/maki/bicycle-11.svg';
  }
  [type = 'castle'],
  [type = 'fort'] {
    background/marker-width: 9;
    background/marker-file: 'data/icons/maki/castle-11.svg';
    marker-width: 9;
    marker-file: 'data/icons/maki/castle-11.svg';
  }
  [type = 'ruins'] {
    background/marker-file: 'data/icons/svg/ruins.svg';
    marker-file: 'data/icons/svg/ruins.svg';
  }
  [type = 'lighthouse'] {
    background/marker-file: 'data/icons/maki/lighthouse-11.svg';
    marker-file: 'data/icons/maki/lighthouse-11.svg';
  }
  [type = 'tower_communication'] {
    background/marker-file: 'data/icons/openstreetmap/communication_tower.svg';
    marker-file: 'data/icons/openstreetmap/communication_tower.svg';
  }
  [type = 'tower_observation'] {
    background/marker-file: 'data/icons/maki/viewpoint-11.svg';
    marker-file: 'data/icons/maki/viewpoint-11.svg';
  }
  [type = 'tower_cooling'] {
    background/marker-width: 7;
    background/marker-file: 'data/icons/openstreetmap/cooling_tower.svg';
    marker-width: 7;
    marker-file: 'data/icons/openstreetmap/cooling_tower.svg';
  }
  [type = 'place_of_worship'] {
    background/marker-file: 'data/icons/openstreetmap/place_of_worship.svg';
    marker-file: 'data/icons/openstreetmap/place_of_worship.svg';

    [religion='christian'] {
      background/marker-width: 4;
      background/marker-file: 'data/icons/openstreetmap/church.svg';
      marker-width: 4;
      marker-file: 'data/icons/openstreetmap/church.svg';
    }
    [religion='jewish'] {
      background/marker-width: 4;
      background/marker-file: 'data/icons/openstreetmap/synagogue.svg';
      marker-width: 4;
      marker-file: 'data/icons/openstreetmap/synagogue.svg';
    }
    [religion='muslim'] {
      background/marker-width: 4;
      background/marker-file: 'data/icons/openstreetmap/mosque.svg';
      marker-width: 4;
      marker-file: 'data/icons/openstreetmap/mosque.svg';
    }
    [religion='buddhist'] {
      background/marker-file: 'data/icons/maki/religious-buddhist-11.svg';
      marker-file: 'data/icons/maki/religious-buddhist-11.svg';
    }
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
  text-placements: 'S,N,E,W,NE,NW,SE,SW';
  text-dx: 10;
  text-dy: 8;

  [place = 'city'] {
    text-transform: uppercase;
  }

  [place = 'city'],
  [place = 'town'] {
    text-face-name: @font-bold;
  }

  [place = 'city'] {
    text-size: 14;
  }
  [place = 'town'] {
    text-size: 12;
  }
  [place = 'village'] {
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
  [type = 'tertiay'],
  [type = 'secondary'],
  [type = 'primary'],
  [type = 'trunk'],
  [type = 'motorway'] {
    text-name: '[ref]';
    text-size: 8;
    text-face-name: @font;
    text-fill: white;
    text-halo-radius: 1.0;
    text-min-path-length: 70;
    text-min-distance: 100;
    text-spacing: 100;
    text-placement: line;

    [type = 'tertiary'] {
      text-size: 7;
    }

    [type = 'tertiary'] {
      text-halo-fill: rgb(82, 82, 82);
    }
    [type = 'secondary'] {
      text-halo-fill: rgb(99, 99, 6);
    }
    [type = 'primary'] {
      text-halo-fill: rgb(168, 109, 25);
    }
    [type = 'trunk'] {
      text-halo-fill: rgb(115, 35, 17);
    }
    [type = 'motorway'] {
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

#scale {
  line-width: 1.0;
  line-color: black;

  ::marker {
    marker-placement: vertex-first;
    marker-allow-overlap: true;
    marker-width: 2;
    marker-fill: black;
  }

  ::text {
    text-name: '[value]';
    text-fill: black;
    text-face-name: @font;
    text-size: 8;
    text-halo-fill: rgba(255, 255, 255, 0.7);
    text-halo-radius: 1.0;
    text-placement: vertex;
    text-dy: 6;
    text-align: left;
    text-allow-overlap: true;
  }
}