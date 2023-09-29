administrative_boundaries = osm2pgsql.define_way_table('administrative_boundaries', {
    { column = 'way', type = 'multilinestring' },
    { column = 'admin_level', type = 'integer' },
})
national_parks = osm2pgsql.define_way_table('national_parks', {
    { column = 'way', type = 'multipolygon' },
})

function osm2pgsql.process_relation(object)
    local tags = object.tags

    -- Administrative boundaries: Levels 0 to 6 are included which has (super-)country
    --   and state administrative borders
    local administrative_admin_level_values = osm2pgsql.make_check_values_func({'0', '1', '2', '3', '4', '5', '6'})
    if tags.boundary == 'administrative'
        and administrative_admin_level_values(tags.admin_level)
    then
        administrative_boundaries:insert({
            way = object:as_multilinestring(),
            admin_level = tags.admin_level,
        })
    end

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