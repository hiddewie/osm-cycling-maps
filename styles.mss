// Fonts
// Taken from https://github.com/gravitystorm/openstreetmap-carto/blob/2868dcad56b7c77f5978637bc23c2156edfe0234/style/fonts.mss
@font: "Noto Sans Regular",
       "Noto Sans CJK JP Regular",
       "Noto Sans Adlam Regular", "Noto Sans Adlam Unjoined Regular",
       "Noto Sans Armenian Regular",
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
       "Noto Naskh Arabic UI Regular",
       "DejaVu Sans Book",
       "HanaMinA Regular",
       "HanaMinB Regular",
       "Unifont Medium",
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

// Palette

@black: rgb(30, 30, 30);
@light-gray: rgb(158, 158, 158);
@gray: rgb(120, 120, 120);
@medium-gray: rgb(105, 105, 105);
@dark-gray: rgb(82, 82, 82);
@white: rgb(255, 255, 255);
@feint-green: rgb(222, 245, 198);
@ocre: rgb(145, 132, 83);
@light-ocre: lighten(@ocre, 40%);
@light-red: rgb(255, 51, 51);
@dark-red: rgb(180, 30, 0);
@light-green: rgb(0, 219, 68);
@light-yellow: rgb(232, 232, 16);
@transparent-light-yellow: rgba(255, 255, 220, 0.8);
@yellow: rgb(255, 210, 80);
@orange: rgb(219, 143, 35);
@blue: rgb(53, 134, 212);
@light-blue: lighten(@blue, 30%);
@dark-blue: darken(@blue, 30%);
@purple: rgb(176, 58, 240);

// Colors

@forest: @feint-green;

@contour: @ocre;
@contour-label-halo: @white;

@residential: @light-ocre;
@military: @light-red;

@admin-background: @light-green;
@admin-boundaries: darken(@light-green, 50%);

@cycling-network: @yellow;

@waterway: @blue;
@water: @light-blue;
@ferry: @dark-blue;

@track: @medium-gray;
@cycle: @purple;
@cycle-border: @white;
@unclassified: @white;
@unclassified-border: @dark-gray;
@tertiary: @unclassified;
@tertiary-border: @unclassified-border;
@secondary: @light-yellow;
@secondary-border: darken(@light-yellow, 30%);
@primary: @orange;
@primary-border: darken(@orange, 30%);
@trunk: @light-gray;
@trunk-border: @white;
@highway: @gray;
@highway-border: @white;

@road-label: white;
@road-label-tertiary-halo: darken(@tertiary, 30%);
@road-label-secondary-halo: darken(@secondary, 30%);
@road-label-primary-halo: darken(@primary, 30%);
@road-label-trunk-halo: darken(@trunk, 30%);
@road-label-motorway-halo: @black;

@rail-dark: @black;
@rail-light: @white;
@rail-preserved-dark: darken(@medium-gray, 30%);
@rail-preserved-light: lighten(@medium-gray, 30%);

@cycling-node: @black;
@cycling-node-label: @black;
@cycling-node-label-halo: @transparent-light-yellow;

@poi: @dark-red;
@poi-label-halo: @transparent-light-yellow;

@power: @light-gray;

@place: @black;
@place-halo: @transparent-light-yellow;

@scale-copyright: @black;
@scale-copyright-halo: @transparent-light-yellow;

// Layers

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
  line-color: @contour;
  line-smooth: 1.0;
  comp-op: multiply;

  [boundary='no'] {
    line-opacity: 0.3;
    line-width: 0.5;
  }

  [boundary='yes'] {
    line-opacity: 0.5;
    line-width: 1.0;
  }
}

#landuse-foreground {
  [type = 'residential'] {
    polygon-fill: @residential;
  }

  [type = 'military'] {
    polygon-pattern-file: url('data/background/military.svg');
    polygon-pattern-comp-op: multiply;
    polygon-pattern-alignment: global;
    line-color: @military;
    line-opacity: 0.333;
    line-width: 1.5;
  }
}

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
  line-color: @cycling-network;
  line-width: 7.0;
  line-cap: round;
}

#waterways {
  line-color: @waterway;
}

#water {
  polygon-fill: @water;
  line-width: 0.5;
  line-color: @water;
}

#ferry {
  line-width: 1.0;
  line-color: @ferry;
  line-dasharray: 4, 3;
}

#springs {
  marker-width: 3;
  marker-fill: @water;
  marker-line-color: @waterway;
  marker-line-width: 1.0;
}

#aeroway {
  line-color: @highway;
  line-cap: square;
  line-width: 5;
}

#railways {
  line-color: @rail-dark;
  line-width: 1.5;
  line-cap: square;

  overlay/line-color: @rail-light;
  overlay/line-width: 1;
  overlay/line-cap: square;

  dash/line-color: @rail-dark;
  dash/line-width: 1;
  dash/line-dasharray: 5, 5;
  dash/line-cap: square;

  [railway = 'preserved'] {
    line-color: @rail-preserved-dark;

    overlay/line-width: 0;
    dash/line-color: @rail-preserved-light;
    dash/line-dasharray: 5, 2;
  }
}

@road-width-small: 1.2;
@road-width-medium: 1.8;
@road-width-large: 2.6;
@road-border-width: 0.7;

#roads::track {
  [type = 'track'] {
    line-width: @road-width-small;
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
  // Widths

  [type = 'residential'],
  [type = 'cycleway'] {
    line-width: @road-width-small + 2 * @road-border-width;
  }

  [type = 'service'],
  [type = 'unclassified'],
  [type = 'secondary'],
  [type = 'secondary_link'],
  [type = 'primary'],
  [type = 'primary_link'] {
    line-width: @road-width-medium + 2 * @road-border-width;
  }

  [type = 'tertiary'],
  [type = 'trunk'],
  [type = 'trunk_link'],
  [type = 'motorway'],
  [type = 'motorway_link'] {
    line-width: @road-width-large + 2 * @road-border-width;
  }

  // Colors

  [type = 'residential'] {
    line-color: @unclassified-border;
  }

  [type = 'service'],
  [type = 'unclassified'] {
    line-color: @unclassified-border;
  }

  [type = 'cycleway'] {
    line-color: @cycle-border;
  }
  [type = 'tertiary'] {
    line-color: @tertiary-border;
  }

  [type = 'secondary'],
  [type = 'secondary_link'] {
    line-color: @secondary-border;
  }

  [type = 'primary'],
  [type = 'primary_link'] {
    line-color: @primary-border;
  }

  [type = 'trunk'],
  [type = 'trunk_link'] {
    line-color: @trunk-border;
  }

  [type = 'motorway'],
  [type = 'motorway_link'] {
    line-color: @highway-border;
  }
}

#roads::fill {
  // Widths

  [type = 'residential'],
  [type = 'cycleway'] {
    line-width: @road-width-small;
  }

  [type = 'service'],
  [type = 'unclassified'],
  [type = 'secondary'],
  [type = 'secondary_link'],
  [type = 'primary'],
  [type = 'primary_link'] {
    line-width: @road-width-medium;
  }

  [type = 'tertiary'],
  [type = 'trunk'],
  [type = 'trunk_link'],
  [type = 'motorway'],
  [type = 'motorway_link'] {
    line-width: @road-width-large;
  }

  // Colors

  [type = 'secondary_link'] {
    line-color: @secondary;
  }

  [type = 'primary_link'] {
    line-color: @primary;
  }

  [type = 'trunk_link'] {
    line-color: @trunk;
  }

  [type = 'motorway_link'] {
    line-color: @highway;
  }

  [type = 'residential'] {
    line-color: @unclassified;
  }

  [type = 'service'],
  [type = 'unclassified'] {
    line-color: @unclassified;
  }

  [type = 'cycleway'] {
    line-color: @cycle;
  }

  [type = 'tertiary'] {
    line-color: @tertiary;
  }

  [type = 'secondary'] {
    line-color: @secondary;
  }

  [type = 'primary'] {
    line-color: @primary;
  }

  [type = 'trunk'] {
    line-color: @trunk;
  }

  [type = 'motorway'] {
    line-color: @highway;
  }
}

#cycling-nodes {
  marker-width: 1.5;
  marker-fill: @cycling-node;
}

#transport {
  background/marker-width: 10;
  background/marker-fill: @poi;
  background/marker-ignore-placement: true;
  background/marker-line-color: white;
  background/marker-line-width: 2.0;

  marker-width: 10;
  marker-fill: @poi;

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
  line-color: @power;
  line-width: 1.0;
}

#power-pole {
  marker-file: 'data/icons/maki/square-11.svg';
  marker-width: 2;
  marker-fill: @power;
  marker-ignore-placement: true;
}

#poi {
  background/marker-width: 10;
  background/marker-fill: @poi;
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
  marker-fill: @poi;

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
  text-fill: @place;
  text-halo-radius: 1.0;
  text-halo-fill: @place-halo;
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
  text-fill: @cycling-node-label;
  text-halo-radius: 1.0;
  text-halo-fill: @cycling-node-label-halo;
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
    text-fill: @road-label;
    text-halo-radius: 1.0;
    text-min-path-length: 70;
    text-min-distance: 100;
    text-spacing: 100;
    text-placement: line;

    [type = 'tertiary'] {
      text-size: 7;
    }

    [type = 'tertiary'] {
      text-halo-fill: @road-label-tertiary-halo;
    }
    [type = 'secondary'] {
      text-halo-fill: @road-label-secondary-halo;
    }
    [type = 'primary'] {
      text-halo-fill: @road-label-primary-halo;
    }
    [type = 'trunk'] {
      text-halo-fill: @road-label-trunk-halo;
    }
    [type = 'motorway'] {
      text-halo-fill: @road-label-motorway-halo;
    }
  }
}

#poi::labels {
  [type = 'mountain_pass'],
  [type = 'peak'] {
    text-name: '[ele]';
    text-size: 7;
    text-face-name: @font-italic;
    text-fill: @poi;
    text-halo-radius: 1.0;
    text-halo-fill: @poi-label-halo;
    text-dy: 7;

    [type = 'peak'] {
      text-dy: 5;
    }
  }
}

#contours {
  [boundary='yes']::label {
    text-name: '[height]';
    text-fill: @contour;
    text-face-name: @font;
    text-size: 6;
    text-halo-fill: @contour-label-halo;
    text-halo-radius: 1.0;
    text-placement: line;
    text-min-path-length: 50;
  }
}

#scale {
  line-width: 1.0;
  line-color: @scale-copyright;

  ::marker {
    marker-placement: vertex-first;
    marker-allow-overlap: true;
    marker-width: 2;
    marker-fill: @scale-copyright;
  }

  ::text {
    text-name: '[value]';
    text-fill: @scale-copyright;
    text-face-name: @font;
    text-size: 8;
    text-halo-fill: @scale-copyright-halo;
    text-halo-radius: 1.0;
    text-placement: vertex;
    text-dy: 6;
    text-align: left;
    text-allow-overlap: true;
  }
}

#copyright {
  text-name: '[label]';
  text-fill: @scale-copyright;
  text-face-name: @font;
  text-size: 8;
  text-halo-fill: @scale-copyright-halo;
  text-halo-radius: 1.0;
  text-allow-overlap: true;
  text-horizontal-alignment: right;
}