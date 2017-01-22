$(function ()
{
    $('input').on('change', function (event)
    {
        var $element   = $(event.target),
            $container = $element.closest('.example');

        if (!$element.data('materialtags'))
        {
            return;
        }

        var val = $element.val();
        if (val === null)
        {
            val = "null";
        }
        $('code', $('pre.val', $container)).html(($.isArray(val) ? JSON.stringify(val) : "\"" + val.replace('"', '\\"') + "\""));
        $('code', $('pre.items', $container)).html(JSON.stringify($element.materialtags('items')));

    }).trigger('change');
});