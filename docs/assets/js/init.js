/**
 * Create a foods Bloodhound
 *
 * @type {Bloodhound}
 */
var foods = new Bloodhound({
    datumTokenizer : Bloodhound.tokenizers.obj.whitespace('text'),
    queryTokenizer : Bloodhound.tokenizers.whitespace,
    prefetch       : 'assets/data/foods.json'
});
foods.initialize();

/**
 * Objects as tags
 */
elt = $('#example_objects input.object-tag-input');
elt.materialtags({
    itemValue   : 'value',
    itemText    : 'text',
    typeaheadjs : {
        name       : 'foods',
        displayKey : 'text',
        source     : foods.ttAdapter()
    }
});