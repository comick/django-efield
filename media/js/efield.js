var Efield = {
	all_counter : 0,
	group_counter : new Array(),
	edit : function(field, group) {
		Efield.all_counter++;
		$('.efield-save-all.efield-hidden.efield-save-all-general').removeClass('efield-hidden');
		if (group) {
			$('.efield-save-all.efield-hidden.efield-group-' + group).removeClass('efield-hidden');
			Efield.group_counter[group] ? Efield.group_counter[group]++ : Efield.group_counter[group] = 0;
		}
		$('#' + field + 'v').addClass('efield-hidden');
		$('#' + field + 'f > .efield-error').addClass('efield-hidden');
		$('#' + field + 'f').removeClass('efield-hidden');
	},
	save_success : function(data) {
		field = $(this)[0].field;
		group = $(this)[0].group;
		trigger = $(this)[0].trigger;
		if (--Efield.all_counter <= 0){
			$('.efield-save-all:not(.efield-hidden).efield-save-all-general').addClass('efield-hidden');
		}	
		if (group && --Efield.group_counter[group] <= 0) {
			$('.efield-save-all:not(.efield-hidden).efield-group-' + group).addClass('efield-hidden');
		}
		$('#' + field + 'f').addClass('efield-hidden');
		$('#' + field + 'v').html(data);
		$('#' + field + 'v').removeClass('efield-hidden');
		if (trigger) {
			trigger(data);
		}
	},
	save_error : function(request) {
		field = $(this)[0].field;
		$('#' + field + 'f > .efield-error').html(request.responseText);
		$('#' + field + 'f > .efield-error').removeClass('efield-hidden');
	},
	save : function(field, options) {
		$.ajax( {
			type : 'POST',
			context : {
				field : field,
				group: options.group,
				trigger: options.trigger
			},
			url : '/efield/',
			data : $('#' + field + 'f').serialize(),
			success : Efield.save_success,
			error : Efield.save_error
		});
	},
	save_all : function(group) {
		sel = (group != null) ? '.efield-group-' + group : '';
		$(sel + '.efield-form:not(.efield-hidden)').each(
				function(index, element) {
					Efield.save(element.id.substr(0, element.id.length - 1), group);
				});
	}
}