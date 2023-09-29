landuse_background = osm2pgsql.define_way_table('landuse_background', {
    { column = 'way', type = 'multipolygon' },
    { column = 'type', type = 'text' },
})
landuse_foreground = osm2pgsql.define_way_table('landuse_foreground', {
    { column = 'way', type = 'multipolygon' },
    { column = 'type', type = 'text' },
})
waterways = osm2pgsql.define_way_table('waterways', {
    { column = 'way', type = 'linestring' },
})
water = osm2pgsql.define_way_table('water', {
    { column = 'way', type = 'multipolygon' },
})
administrative_boundaries = osm2pgsql.define_way_table('administrative_boundaries', {
    { column = 'way', type = 'multilinestring' },
    { column = 'admin_level', type = 'integer' },
})
national_parks = osm2pgsql.define_way_table('national_parks', {
    { column = 'way', type = 'multipolygon' },
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

function process_landuse_foreground(object)
    local tags = object.tags
    local landuse_values = osm2pgsql.make_check_values_func({'residential', 'industrial', 'military'})
    if landuse_values(tags.landuse) then
        landuse_foreground:insert({
            way = object:as_multipolygon(),
            type = tags.landuse,
        })
    end
end

function process_waterways(object)
    local tags = object.tags
    local waterway_values = osm2pgsql.make_check_values_func({'river', 'stream', 'canal', 'drain'})
    if waterway_values(tags.waterway)
        and tags.tunnel ~= 'yes'
    then
        waterways:insert({
            way = object:as_linestring(),
        })
    end
end

function process_water(object)
    local tags = object.tags
    local landuse_values = osm2pgsql.make_check_values_func({'reservoir', 'basin'})
    if tags.natural == 'water'
        or tags.waterway == 'riverbank'
        or landuse_values(tags.landuse)
    then
        water:insert({
            way = object:as_multipolygon(),
        })
    end
end

-- Administrative boundaries: Levels 0 to 6 are included which has (super-)country
--   and state administrative borders
function process_administrative_boundary(object)
    local tags = object.tags
    local administrative_admin_level_values = osm2pgsql.make_check_values_func({'0', '1', '2', '3', '4', '5', '6'})
    if tags.boundary == 'administrative'
        and administrative_admin_level_values(tags.admin_level)
    then
        administrative_boundaries:insert({
            way = object:as_multilinestring(),
            admin_level = tags.admin_level,
        })
    end
end

function process_national_park(object)
    local tags = object.tags
    local national_park_protect_class_values = osm2pgsql.make_check_values_func({'1', '1a', '1b', '2', '3', '4', '5', '6'})
    if (tags.boundary == 'national_park'
            or (tags.boundary == 'protected_area' and national_park_protect_class_values(tags.protect_class))
        and object:as_multipolygon():spherical_area() >= 5e5)
    then
        national_parks:insert({
            way = object:as_multipolygon(),
        })
    end
end

function osm2pgsql.process_way(object)
    process_landuse_background(object)
    process_landuse_foreground(object)
    process_waterways(object)
    process_water(object)
end

function osm2pgsql.process_relation(object)
    process_landuse_background(object)
    process_landuse_foreground(object)
    process_water(object)
    process_administrative_boundary(object)
    process_national_park(object)
end