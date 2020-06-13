// Fonts
// Taken from https://github.com/gravitystorm/openstreetmap-carto/blob/2868dcad56b7c77f5978637bc23c2156edfe0234/style/fonts.mss
@font: "Noto Sans Regular",
       "Noto Sans CJK JP Regular",
       "Noto Sans Adlam Regular", "Noto Sans Adlam Unjoined Regular",
       "Noto Sans Armenian Regular",
       "Noto Sans Balinese Regular",
       "Noto Sans Bamum Regular",
       "Noto Sans Batak Regular",
       "Noto Sans Bengali UI Regular",
       "Noto Sans Buginese Regular",
       "Noto Sans Buhid Regular",
       "Noto Sans Canadian Aboriginal Regular",
       "Noto Sans Chakma Regular",
       "Noto Sans Cham Regular",
       "Noto Sans Cherokee Regular",
       "Noto Sans Coptic Regular",
       "Noto Sans Devanagari UI Regular",
       "Noto Sans Ethiopic Regular",
       "Noto Sans Georgian Regular",
       "Noto Sans Gujarati UI Regular",
       "Noto Sans Gurmukhi UI Regular",
       "Noto Sans Hanunoo Regular",
       "Noto Sans Hebrew Regular",
       "Noto Sans Javanese Regular",
       "Noto Sans Kannada UI Regular",
       "Noto Sans Kayah Li Regular",
       "Noto Sans Khmer UI Regular",
       "Noto Sans Lao UI Regular",
       "Noto Sans Lepcha Regular",
       "Noto Sans Limbu Regular",
       "Noto Sans Lisu Regular",
       "Noto Sans Malayalam UI Regular",
       "Noto Sans Mandaic Regular",
       "Noto Sans Mongolian Regular",
       "Noto Sans Myanmar UI Regular",
       "Noto Sans New Tai Lue Regular",
       "Noto Sans NKo Regular",
       "Noto Sans Ol Chiki Regular",
       "Noto Sans Oriya UI Regular",
       "Noto Sans Osage Regular",
       "Noto Sans Osmanya Regular",
       "Noto Sans Samaritan Regular",
       "Noto Sans Saurashtra Regular",
       "Noto Sans Shavian Regular",
       "Noto Sans Sinhala UI Regular",
       "Noto Sans Sinhala Regular",
       "Noto Sans Sundanese Regular",
       "Noto Sans Symbols Regular",
       "Noto Sans Symbols2 Regular",
       "Noto Sans Syriac Eastern Regular",
       "Noto Sans Tagalog Regular",
       "Noto Sans Tagbanwa Regular",
       "Noto Sans Tai Le Regular",
       "Noto Sans Tai Tham Regular",
       "Noto Sans Tai Viet Regular",
       "Noto Sans Tamil UI Regular",
       "Noto Sans Telugu UI Regular",
       "Noto Sans Thaana Regular",
       "Noto Sans Thai UI Regular",
       "Noto Sans Tibetan Regular",
       "Noto Sans Tifinagh Regular",
       "Noto Sans Vai Regular",
       "Noto Sans Yi Regular",
       "Noto Sans Arabic UI Regular",
       "Noto Emoji Regular",
       "Noto Naskh Arabic UI Regular",
       "DejaVu Sans Book",
       "HanaMinA Regular",
       "HanaMinB Regular",
       "Unifont Medium",
       "unifont Medium",
       "Unifont Upper Medium";

// A bold style is available for almost all scripts. Bold text is heavier than
// regular text and can be used for emphasis. Fallback is a regular style.
@font-bold: "Noto Sans Bold",
            "Noto Sans CJK JP Bold",
            "Noto Sans Armenian Bold",
            "Noto Sans Bengali UI Bold",
            "Noto Sans Cham Bold",
            "Noto Sans Cherokee Bold",
            "Noto Sans Devanagari UI Bold",
            "Noto Sans Ethiopic Bold",
            "Noto Sans Georgian Bold",
            "Noto Sans Gujarati UI Bold",
            "Noto Sans Gurmukhi UI Bold",
            "Noto Sans Hebrew Bold",
            "Noto Sans Kannada UI Bold",
            "Noto Sans Khmer UI Bold",
            "Noto Sans Lao UI Bold",
            "Noto Sans Malayalam UI Bold",
            "Noto Sans Myanmar UI Bold",
            "Noto Sans Oriya UI Bold",
            "Noto Sans Sinhala UI Bold",
            "Noto Sans Sinhala Bold",
            "Noto Sans Symbols Bold",
            "Noto Sans Tamil UI Bold",
            "Noto Sans Telugu UI Bold",
            "Noto Sans Thaana Bold",
            "Noto Sans Thai UI Bold",
            "Noto Sans Tibetan Bold",
            "Noto Sans Arabic UI Bold",
            "Noto Naskh Arabic UI Bold",
            "DejaVu Sans Bold";

// Italics are only available for the base font, not the other scripts.
// For a considerable number of labels this style will make no difference to the regular style.
@font-italic: "Noto Sans Italic",
              @font; // for non-latin characters

@font-bold-italic: "Noto Sans Bold Italic",
                   @font; // for non-latin characters


// Colors
@forest: rgb(222, 245, 198);

#landuse-background {
  [type = 'forest'] {
    polygon-fill: @forest;
  }
}

#shade {
  raster-scaling: lanczos;
  raster-comp-op: multiply;
  raster-opacity: 0.75;
}

#contours {
  [boundary='no'] {
    line-color: rgba(145, 132, 83, 0.3);
    line-width: 0.5;
    line-smooth: 1.0;
  }

  [boundary='yes'] {
    line-color: rgba(145, 132, 83, 0.5);
    line-width: 1.0;
    line-smooth: 1.0;
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

  [railway = 'preserved'] {
    line-color: rgb(100, 100, 100);

    overlay/line-width: 0;
    dash/line-color: rgb(200, 200, 200);
    dash/line-dasharray: 5, 2;
  }
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
  marker-width: 1.5;
  marker-fill: rgb(30, 30, 30);
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
  [type = 'ruins'],
  [type = 'wind_power'] {
    background/marker-line-width: 50.0;
  }

  [type = 'mountain_pass'] {
    background/marker-line-width: 0.5;
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
    background/marker-width: 9;
    background/marker-file: 'data/icons/maki/hospital-11.svg';
    marker-width: 9;
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
  [type = 'mountain_pass'] {
    background/marker-width: 8;
    background/marker-file: 'data/icons/openstreetmap/mountain_pass.svg';
    marker-width: 8;
    marker-file: 'data/icons/openstreetmap/mountain_pass.svg';
  }
  [type = 'peak'] {
    background/marker-width: 5;
    background/marker-file: 'data/icons/svg/triangle.svg';
    marker-width: 5;
    marker-file: 'data/icons/svg/triangle.svg';
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
  [type = 'wind_power'] {
    background/marker-width: 9;
    background/marker-file: 'data/icons/svg/wind_generator.svg';
    background/marker-transform: 'translate(0, -4)';
    marker-width: 9;
    marker-file: 'data/icons/svg/wind_generator.svg';
    marker-transform: 'translate(0, -4)';
  }
  [type = 'place_of_worship'] {
    background/marker-width: 4;
    background/marker-file: 'data/icons/openstreetmap/religion_unknown.svg';
    marker-width: 4;
    marker-file: 'data/icons/openstreetmap/religion_unknown.svg';

    [religion='christian'] {
      background/marker-width: 4;
      background/marker-file: 'data/icons/openstreetmap/church.svg';
      background/marker-transform: 'translate(0, -2)';
      marker-width: 4;
      marker-file: 'data/icons/openstreetmap/church.svg';
      marker-transform: 'translate(0, -2)';
    }
    [religion='jewish'] {
      background/marker-width: 4;
      background/marker-file: 'data/icons/openstreetmap/synagogue.svg';
      background/marker-transform: 'translate(0, -2)';
      marker-width: 4;
      marker-file: 'data/icons/openstreetmap/synagogue.svg';
      marker-transform: 'translate(0, -2)';
    }
    [religion='muslim'] {
      background/marker-width: 4;
      background/marker-file: 'data/icons/openstreetmap/mosque.svg';
      background/marker-transform: 'translate(0, -2)';
      marker-width: 4;
      marker-file: 'data/icons/openstreetmap/mosque.svg';
      marker-transform: 'translate(0, -2)';
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
  text-face-name: @font-italic;
  text-fill: black;
  text-halo-radius: 1.0;
  text-halo-fill: rgba(255, 226, 143, 0.7);
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

#poi::labels {
  [type = 'mountain_pass'],
  [type = 'peak'] {
    text-name: '[ele]';
    text-size: 7;
    text-face-name: @font-italic;
    text-fill: purple;
    text-halo-radius: 1.0;
    text-halo-fill: rgba(255, 255, 220, 0.7);
    text-dy: 7;

    [type = 'peak'] {
      text-dy: 5;
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

#copyright {
  text-name: '[label]';
  text-fill: black;
  text-face-name: @font;
  text-size: 8;
  text-halo-fill: rgba(255, 255, 255, 0.7);
  text-halo-radius: 1.0;
  text-allow-overlap: true;
  text-horizontal-alignment: right;
}