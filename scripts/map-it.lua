boundaries = osm2pgsql.define_way_table('boundaries', {
    { column = 'way', type = 'multilinestring' },
    { column = 'boundary', type = 'text' },
    { column = 'admin_level', type = 'integer' },
})

local national_park_values = osm2pgsql.make_check_values_func({'0', '1', '2', '3', '4', '5', '6'})
function osm2pgsql.process_relation(object)
    local tags = object.tags
    if tags.boundary == 'administrative' and national_park_values(tags.national_park) then
        boundaries:insert({
            way = object:as_multilinestring(),
            boundary = tags.boundary,
            admin_level = tags.admin_level,
        })
    end
end