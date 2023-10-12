function dump(o)
   if type(o) == 'table' then
      local s = '{ '
      for k,v in pairs(o) do
         if type(k) ~= 'number' then k = '"'..k..'"' end
         s = s .. '['..k..'] = ' .. dump(v) .. ','
      end
      return s .. '} '
   else
      return tostring(o)
   end
end

local landuse_background = osm2pgsql.define_way_table('landuse_background', {
    { column = 'way', type = 'multipolygon' },
    { column = 'type', type = 'text' },
})
local landuse_foreground = osm2pgsql.define_way_table('landuse_foreground', {
    { column = 'way', type = 'multipolygon' },
    { column = 'type', type = 'text' },
})
local waterways = osm2pgsql.define_way_table('waterways', {
    { column = 'way', type = 'linestring' },
})
local water = osm2pgsql.define_way_table('water', {
    { column = 'way', type = 'multipolygon' },
})
local dams = osm2pgsql.define_way_table('dams', {
    { column = 'way', type = 'linestring' },
    { column = 'type', type = 'text' },
})
local administrative_boundaries = osm2pgsql.define_way_table('administrative_boundaries', {
    { column = 'way', type = 'multilinestring' },
    { column = 'admin_level', type = 'integer' },
})
local national_parks = osm2pgsql.define_way_table('national_parks', {
    { column = 'way', type = 'multipolygon' },
})
local ferries = osm2pgsql.define_way_table('ferries', {
    { column = 'way', type = 'multilinestring' },
})
local power_lines = osm2pgsql.define_way_table('power_lines', {
    { column = 'way', type = 'multilinestring' },
})
local power_poles = osm2pgsql.define_node_table('power_poles', {
    { column = 'way', type = 'point' },
})
local tunnels = osm2pgsql.define_way_table('tunnels', {
    { column = 'way', type = 'linestring' },
    { column = 'layer', type = 'integer' },
    { column = 'type', type = 'text' },
})
local aeroways = osm2pgsql.define_way_table('aeroways', {
    { column = 'way', type = 'linestring' },
})
local roads = osm2pgsql.define_way_table('roads', {
    { column = 'way', type = 'linestring' },
    { column = 'type', type = 'text' },
    { column = 'railway', type = 'text' },
    { column = 'bicycle', type = 'boolean' },
    { column = 'tracktype', type = 'text' },
    { column = 'layer', type = 'integer' },
})
local cycling_nodes = osm2pgsql.define_node_table('cycling_nodes', {
    { column = 'way', type = 'point' },
    { column = 'ref', type = 'text' },
})
local cycling_routes = osm2pgsql.define_way_table('cycling_routes', {
    { column = 'way', type = 'multilinestring' },
})
local transport = osm2pgsql.define_table({
    name = 'transport',
    ids = { type = 'any', id_column = 'osm_id' },
    columns = {
        { column = 'way', type = 'point' },
        { column = 'type', type = 'text' },
    },
})

function process_landuse_background(object)
    local tags = object.tags
    if tags.landuse == 'forest'
        or tags.natural == 'wood'
    then
        landuse_background:insert({
            way = object:as_multipolygon(),
            type = 'forest',
        })
    end
    if tags.aeroway == 'aerodrome' then
        landuse_background:insert({
            way = object:as_multipolygon(),
            type = 'aerodrome',
        })
    end
end

local landuse_foreground_values = osm2pgsql.make_check_values_func({'residential', 'industrial', 'military'})
function process_landuse_foreground(object)
    local tags = object.tags
    if landuse_foreground_values(tags.landuse) then
        landuse_foreground:insert({
            way = object:as_multipolygon(),
            type = tags.landuse,
        })
    end
end

local waterway_values = osm2pgsql.make_check_values_func({'river', 'stream', 'canal', 'drain'})
function process_waterways(object)
    local tags = object.tags
    if waterway_values(tags.waterway)
        and tags.tunnel ~= 'yes'
    then
        waterways:insert({
            way = object:as_linestring(),
        })
    end
end

local water_landuse_values = osm2pgsql.make_check_values_func({'reservoir', 'basin'})
function process_water(object)
    local tags = object.tags
    if tags.natural == 'water'
        or tags.waterway == 'riverbank'
        or water_landuse_values(tags.landuse)
    then
        water:insert({
            way = object:as_multipolygon(),
        })
    end
end

function process_dam(object)
    local tags = object.tags
    if tags.waterway == 'dam' then
        local type = object.is_closed and 'polygon' or 'line'
        dams:insert({
            way = object:as_linestring(),
            type = type,
        })
    end
end

-- Administrative boundaries: Levels 0 to 6 are included which has (super-)country
--   and state administrative borders
local administrative_admin_level_values = osm2pgsql.make_check_values_func({'0', '1', '2', '3', '4', '5', '6'})
function process_administrative_boundary(object)
    local tags = object.tags
    if tags.boundary == 'administrative'
        and administrative_admin_level_values(tags.admin_level)
    then
        administrative_boundaries:insert({
            way = object:as_multilinestring(),
            admin_level = tags.admin_level,
        })
    end
end

local national_park_protect_class_values = osm2pgsql.make_check_values_func({'1', '1a', '1b', '2', '3', '4', '5', '6'})
function process_national_park(object)
    local tags = object.tags
    if (tags.boundary == 'national_park'
            or (tags.boundary == 'protected_area' and national_park_protect_class_values(tags.protect_class))
        and object:as_multipolygon():spherical_area() >= 5e5)
    then
        national_parks:insert({
            way = object:as_multipolygon(),
        })
    end
end

function process_ferry(object)
    local tags = object.tags
    if tags.route == 'ferry' then
        ferries:insert({
            way = object:as_multilinestring(),
        })
    end
end

function process_power_line(object)
    local tags = object.tags
    if tags.power == 'line' then
        power_lines:insert({
            way = object:as_multilinestring(),
        })
    end
end

function process_power_pole(object)
    local tags = object.tags
    if tags.power == 'tower' then
        power_poles:insert({
            way = object:as_point(),
        })
    end
end

local tunnel_highway_values = osm2pgsql.make_check_values_func({ 'motorway_link', 'trunk_link', 'secondary_link', 'primary_link', 'motorway', 'trunk', 'cycleway', 'tertiary', 'secondary', 'primary' })
local tunnel_railway_values = osm2pgsql.make_check_values_func({ 'rail', 'narrow_gauge' })
local service_values = osm2pgsql.make_check_values_func({ 'crossover', 'spur', 'yard' })
function process_tunnel(object)
    local tags = object.tags
    if tunnel_highway_values(tags.highway)
        and tags.access ~= 'private'
        and tags.tunnel == 'yes'
    then
        tunnels:insert({
            way = object:as_linestring(),
            layer = tags.layer,
            type = tags.highway,
        })
    end
    if tunnel_railway_values(tags.railway)
        and tags.tunnel == 'yes'
        and not service_values(tags.service)
    then
        tunnels:insert({
            way = object:as_linestring(),
            layer = tags.layer,
            type = tags.highway,
        })
    end
end

function process_aeroway(object)
    local tags = object.tags
    if tags.aeroway == 'runway' then
        aeroways:insert({
            way = object:as_linestring(),
        })
    end
end

local road_railway_values = osm2pgsql.make_check_values_func({ 'rail', 'narrow_gauge', 'preserved' })
local road_disallowed_highway_values = osm2pgsql.make_check_values_func({ 'platform', 'construction', 'proposed', 'steps' })
local road_bicycle_values = osm2pgsql.make_check_values_func({ 'yes', 'designated', 'permissive' })
function process_road(object)
    local tags = object.tags
    if tags.highway
        and not road_disallowed_highway_values(tags.highway)
        and tags.access ~= 'private'
        and tags.tunnel ~= 'yes'
    then
        local type = tags.highway
        if tags.bicycle == 'designated' then
            type = 'cycleway'
        elseif tags.highway == 'road' then
            type = 'unclassified'
        elseif tags.highway == 'living_street' then
            type = 'residential'
        end
        roads:insert({
            way = object:as_linestring(),
            type = type,
            bicycle = road_bicycle_values(tags.bicycle),
            tracktype = tags.tracktype,
            layer = tags.layer,
        })
    end
    if road_railway_values(tags.railway)
        and not service_values(tags.service)
        and tags.tunnel ~= 'yes'
    then
        roads:insert({
            way = object:as_linestring(),
            type = 'railway',
            railway = tags.railway,
            bicycle = 'F',
            tracktype = tags.tracktype,
            layer = tags.layer,
        })
    end
end

function process_cycling_node(object)
    local tags = object.tags
    if tags.rcn_ref
        and tags['network:type'] == 'node_network'
    then
        cycling_nodes:insert({
            way = object:as_point(),
            ref = tags.rcn_ref,
        })
    end
end

function process_cycling_route(object)
    local tags = object.tags
    if tags.route == 'bicycle' then
        cycling_routes:insert({
            way = object:as_multilinestring(),
        })
    end
end

local railway_values = osm2pgsql.make_check_values_func({'station', 'halt'})
local disallowed_station_values = osm2pgsql.make_check_values_func({'subway', 'light_rail', 'monorail', 'funicular'})
function process_transport(object)
    local tags = object.tags
    if tags.aeroway == 'aerodrome' then
        transport:insert({
            way = object.type == 'way' and object:as_linestring():centroid() or object:as_point(),
            type = 'aerodrome',
        })
    end
    if railway_values(tags.railway)
        and (not tags.station
            or not disallowed_station_values(tags.station))
    then
        transport:insert({
            way = object.type == 'way' and object:as_linestring():centroid() or object:as_point(),
            type = 'train_station',
        })
    end
    if tags.amenity == 'ferry_terminal' then
        transport:insert({
            way = object.type == 'way' and object:as_linestring():centroid() or object:as_point(),
            type = 'ferry_terminal',
        })
    end
end

function osm2pgsql.process_node(object)
    process_power_pole(object)
    process_cycling_node(object)
    process_transport(object)
end

function osm2pgsql.process_way(object)
    process_landuse_background(object)
    process_landuse_foreground(object)
    process_waterways(object)
    process_water(object)
    process_dam(object)
    process_power_line(object)
    process_tunnel(object)
    process_aeroway(object)
    process_road(object)
    process_transport(object)
end

function osm2pgsql.process_relation(object)
    process_landuse_background(object)
    process_landuse_foreground(object)
    process_water(object)
    process_administrative_boundary(object)
    process_national_park(object)
    process_ferry(object)
    process_cycling_route(object)
end
