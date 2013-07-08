define [
    "ember"
    "cs!sitterfied"
    'data'
    'djangoRestAdapter'
    ], (Em, Sitterfied, DS) ->


    Sitterfied.Store = DS.Store.extend(
        revision: 12
        adapter: DS.DjangoRESTAdapter.create({
            namespace: 'api'
        })
        isDefaultStore:true
    )

    Sitterfied.UserMixin = Em.Mixin.create(
        #django builtins
        #last_login: DS.attr('date')
        is_superuser: DS.attr('boolean')
        username: DS.attr('string')
        first_name: DS.attr('string')
        last_name: DS.attr('string')
        email: DS.attr('string')
        status: DS.attr('string')
        parents_in_network: DS.hasMany('Sitterfied.Parent')
        sitters_in_network: DS.hasMany('Sitterfied.Sitter')
        sitter_groups: DS.hasMany('Sitterfied.Group')
        languages: DS.hasMany('Sitterfied.Language')
        settings  : DS.belongsTo('Sitterfied.Setting')
        bookings: DS.hasMany('Sitterfied.Booking'),
        address1: DS.attr('string')
        address2: DS.attr('string')
        city: DS.attr('string')
        state: DS.attr('string')
        zip: DS.attr('string')
        cell: DS.attr('string')
        reviews: DS.hasMany('Sitterfied.SitterReview')

        sorted_bookings: (() ->
            return this.get('bookings').toArray().sort((booking1, booking2) ->
                if booking1.get('start_date_time') > booking2.get('start_date_time')
                    return 1
                else
                    return -1
            )
        ).property('bookings.@each')
        weeks_since_last_booking: (() ->
            if this.get('sorted_bookings').length == 0
                return 0
            else
                debugger
                most_recent_booking = this.get('sorted_bookings')[0]
        ).property('sorted_bookings')
        days_since_last_booking: (() ->
            if this.get('sorted_bookings').length == 0
                return 0
            else
                debugger
                most_recent_booking = this.get('sorted_bookings')[0]
        ).property('sorted_bookings')
        full_name: ((key, value) ->
            if arguments.length == 1
                return @get('first_name') + ' ' + @get('last_name')

            else
                [first_name, last_name] = value.trim().split(" ", 2)
                this.set('first_name', first_name)
                this.set('last_name', last_name)
                return value
        ).property('first_name', 'last_name')
    )

    Sitterfied.Setting = DS.Model.extend(
        user  : DS.belongsTo('Sitterfied.' + parent_or_sitter)
        #parent specific
        mobile_booking_accepted_denied: DS.attr('boolean')

        #sitter specific
        mobile_new_review : DS.attr('boolean')
        mobile_booking_request: DS.attr('boolean')

        mobile_friend_joined: DS.attr('boolean')
        mobile_groups_added_network: DS.attr('boolean')
        mobile_upcoming_booking_remind: DS.attr('boolean')

        #parent specific
        email_booking_accepted_denied: DS.attr('boolean')

        #sitter specific
        email_new_review : DS.attr('boolean')
        email_booking_request: DS.attr('boolean')

        email_friend_joined: DS.attr('boolean')
        email_groups_added_network: DS.attr('boolean')
        email_upcoming_booking_remind: DS.attr('boolean')

        email_news: DS.attr('boolean')
        email_blog: DS.attr('boolean')
    )

    Sitterfied.Contact = DS.Model.extend(
        #flush out later
    )

    Sitterfied.Group = DS.Model.extend(
        name: DS.attr('string')
    )

    Sitterfied.Parent = DS.Model.extend(Sitterfied.UserMixin,
        emergency_contact : DS.belongsTo('Sitterfied.Contact'),
        physician_contact : DS.belongsTo('Sitterfied.Contact'),
        parking_area : DS.attr('boolean'),
        parking_for_sitter: DS.attr('boolean'),

    )

    Sitterfied.Schedlue = DS.Model.extend(
        sitter: DS.belongsTo('Sitterfied.Sitter'),
        mon_early_morning: DS.attr('boolean')
        tues_early_morning: DS.attr('boolean')
        wed_early_morning: DS.attr('boolean')
        thurs_early_morning: DS.attr('boolean')
        fri_early_morning: DS.attr('boolean')
        sat_early_morning: DS.attr('boolean')
        sun_early_morning: DS.attr('boolean')

        mon_late_morning: DS.attr('boolean')
        tues_late_morning: DS.attr('boolean')
        wed_late_morning: DS.attr('boolean')
        thurs_late_morning: DS.attr('boolean')
        fri_late_morning: DS.attr('boolean')
        sat_late_morning: DS.attr('boolean')
        sun_late_morning: DS.attr('boolean')

        mon_early_afternoon: DS.attr('boolean')
        tues_early_afternoon: DS.attr('boolean')
        wed_early_afternoon: DS.attr('boolean')
        thurs_early_afternoon: DS.attr('boolean')
        fri_early_afternoon: DS.attr('boolean')
        sat_early_afternoon: DS.attr('boolean')
        sun_early_afternoon: DS.attr('boolean')

        mon_late_afternoon: DS.attr('boolean')
        tues_late_afternoon: DS.attr('boolean')
        wed_late_afternoon: DS.attr('boolean')
        thurs_late_afternoon: DS.attr('boolean')
        fri_late_afternoon: DS.attr('boolean')
        sat_late_afternoon: DS.attr('boolean')
        sun_late_afternoon: DS.attr('boolean')

        mon_early_evening: DS.attr('boolean')
        tues_early_evening: DS.attr('boolean')
        wed_early_evening: DS.attr('boolean')
        thurs_early_evening: DS.attr('boolean')
        fri_early_evening: DS.attr('boolean')
        sat_early_evening: DS.attr('boolean')
        sun_early_evening: DS.attr('boolean')

        mon_late_evening: DS.attr('boolean')
        tues_late_evening: DS.attr('boolean')
        wed_late_evening: DS.attr('boolean')
        thurs_late_evening: DS.attr('boolean')
        fri_late_evening: DS.attr('boolean')
        sat_late_evening: DS.attr('boolean')
        sun_late_evening: DS.attr('boolean')

        mon_overnight: DS.attr('boolean')
        tues_overnight: DS.attr('boolean')
        wed_overnight: DS.attr('boolean')
        thurs_overnight: DS.attr('boolean')
        fri_overnight: DS.attr('boolean')
        sat_overnight: DS.attr('boolean')
        sun_overnight: DS.attr('boolean')
    )

    Sitterfied.Sitter = DS.Model.extend(Sitterfied.UserMixin,
        biography: DS.attr('string'),
        gender:  DS.attr('string'),
        id_verified: DS.attr('boolean'),
        id_scanPath: DS.attr('string'),
        live_zip: DS.attr('string'),
        work_zip: DS.attr('string'),
        dob: DS.attr('string'),
        smoker: DS.attr('string'),
        sick: DS.attr('string'),
        will_transport: DS.attr('string'),
        total_exp: DS.attr('number'),
        infant_exp: DS.attr('number'),
        toddler_exp: DS.attr('number'),
        preschool_exp: DS.attr('number'),
        school_age_exp: DS.attr('number'),
        pre_teen_exp: DS.attr('number'),
        teen_exp: DS.attr('number'),

        highest_education: DS.attr('string'),
        last_school: DS.attr('string'),
        current_student: DS.attr('string'),

        schedlue: DS.belongsTo('Sitterfied.Schedlue'),

        major: DS.attr('string'),
        occupation:  DS.attr('string'),

        certification: DS.hasMany('Sitterfied.Certification'),
        other_services: DS.attr('string'),
        one_child_min_rate: DS.attr('number'),
        one_child_max_rate: DS.attr('number'),
        two_child_min_rate: DS.attr('number'),
        two_child_max_rate: DS.attr('number'),
        three_child_min_rate: DS.attr('number'),
        three_child_max_rate: DS.attr('number'),


        special_needs_exp : DS.attr('string')
        extra_exp: DS.attr('string')

        smokers_ok: DS.attr('string'),
        dogs_ok: DS.attr('string'),
        cats_ok: DS.attr('string'),
        other_animals_ok: DS.attr('string'),
        travel_distance: DS.attr('number'),
        has_drivers_licence: DS.attr('string'),


        calc_total_exp: ((value) ->
            return @get('infant_exp') + @get('toddler_exp') + @get('preschool_exp') + @get('school_ageExp') + @get('pre_teenExp') + @get('teen_exp')
        ).property('infant_exp','toddler_exp','preschool_exp', 'school_ageExp', 'pre_teenExp', 'teen_exp')
    )

    Sitterfied.Language = DS.Model.extend(
        language: DS.attr('string'),
    )
    Sitterfied.Certification = DS.Model.extend(
        certification: DS.attr('string'),
    )


    Sitterfied.Child = DS.Model.extend(
        parent: DS.belongsTo('Sitterfied.Parent'),
        name: DS.attr('string'),
        dob: DS.attr('date'),
        school: DS.attr('string'),
        sitter_instructions: DS.attr('string'),
        special_needs: DS.attr('string'),
        allergies: DS.attr('string'),
    )

    Sitterfied.SitterReview = DS.Model.extend(
        parent: DS.belongsTo('Sitterfied.Parent'),
        sitter: DS.belongsTo('Sitterfied.Sitter'),
        recommended: DS.attr('boolean'),
        review: DS.attr('string'),
    )

    Sitterfied.Booking = DS.Model.extend(
        parent: DS.belongsTo('Sitterfied.Parent'),
        sitter: DS.belongsTo('Sitterfied.Sitter'),
        notes: DS.attr('string'),
        respond_by: DS.attr('date'),
        start_date_time: DS.attr('date'),
        stop_date_time: DS.attr('date'),
        child: DS.hasMany("Sitterfied.Child"),
        #emergency_phone: models.Foreign_key('Phone')
        #location: models.Foreign_key('Address')
        booking_status:DS.attr('string'),
    )