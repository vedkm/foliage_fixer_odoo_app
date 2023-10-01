odoo.define('plant_form_tests', function (require) {
    "use strict";

    var FormView = require('web.FormView');
    var testUtils = require('web.test_utils')

    QUnit.module('Plant Form Tests', {
        beforeEach: function () {
            this.data = {
                plant: {
                    fields: {
                        name: { string: 'Name', type: 'char' },
                        family: { string: 'Family', type: 'char' },
                        records: [
                            { id: 1, name: 'Plant 1', family: 'Tomato 1' },
                            { id: 2, name: 'Plant 2', family: 'Tomato 2' }
                        ],
                        function () {
                            QUnit.only('name field test cases', async function(assert) {
                                assert.expect(1)

                                const form = await testUtils.createView({
                                    View: FormView,
                                    model: 'Plant',
                                    data: this.data,
                                    arch: '<form string="Plant">' +
                                        '<group>' +
                                        <field name="name"/> +
                                        <field name="family"/> +
                                        '</group>' +
                                        '</form>',
                                    res_id: 1,
                                });

                                await testUtils.form.clickEdit(form)
                                form.destroy();
                                assert.equal(1, 1)
                            })
                        }
                    }
                }
            }
        }
    })
})