htm = '''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Document</title>
                         <style>
                                .styled-table {

                                    border-collapse: collapse;

                                    margin: 25px 0;
                                    font-size: 5.3em;
                                    font-family: sans-serif;
                                    width : 900;
                                    height:700;
                                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                                }
                                .styled-table thead tr {
                                    background-color: #00a1af;
                                    color: #ffffff;
                                    text-align:center;


                                }
                                .styled-table th,
                        .styled-table td {
                            padding: 12px 15px;
                            text-align:center;
                            font-weight: normal;
                        }
                        .styled-table tbody tr {
                            border-bottom: 1.2px solid #00a1af;
                        }

                        .styled-table tbody tr:nth-of-type(even) {
                            background-color: #f3f3f3;
                        }

                        .styled-table tbody tr:last-of-type {
                            border-bottom: 2px solid #00a1af;
                        }
                        .styled-table tbody tr.active-row {

                            color: #00a1af;
                        }
                            </style>
                        </head>
                         <body id="as12" style="padding:30px; height:fit-content; ">

                             <table class="styled-table" >
                                <thead>
                                    <tr>
                                        <th>متبقي على الاختبار</th>

                                        <th>الى</th>
                                        <th>من</th>
                                        <th>تاريخ الاختبار </th>

                                        <th>اسم القرر</th>
                                        <th>رمز المقرر</th>
                                    </tr>
                                </thead>
                                <tbody>


                                    %s

                                    <!-- and so on... -->
                                </tbody>
                            </table>

                        </body>
                        </html>'''





gpa = '''
          <div class="wrapper itme" style="height: max-content;width: 700px ;" id = "as12" >
            <div class="clash-card barbarian" >
                    <br>

                %s

                %s
                <br>
                <div class="clash-card__unit-name">%s</div>
                <br>
                <div class="clash-card__unit-name">%s</div>
                    <br>

                    <div class="clash-card__unit-stats clash-card__unit-stats--barbarian clearfix">
                    <div class="one-third">
                        <div class="stat">%s<div></div></div>
                        <div class="stat-value">الساعات</div>
                    </div>

                    <div class="one-third">
                        <div class="stat">%s</div>
                        <div class="stat-value">النقاط</div>
                    </div>

                    <div class="one-third no-border">
                        <div class="stat">%s</div>
                        <div class="stat-value">المعدل</div>
                    </div>

                    </div>

                </div> <!-- end clash-card barbarian-->

                </div>

'''



gpaimg = '''
                                    <!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <title>Document</title>
                                        <style>
                                      %s
                                        </style>

                                    </head>
                                    <body>
                                        <div class="slide-container">




                                                %s







                                        </div> <!-- end container -->

                                    </body>
                                    </html>

'''


st = ''' @import url(https://fonts.googleapis.com/css?family=Lato:400,700,900);
                        *, *:before, *:after {
                            box-sizing: border-box;
                        }
                        body {
                            /* background: linear-gradient(to bottom, rgba(140, 122, 122, 1) 0%, rgba(175, 135, 124, 1) 65%, rgba(175, 135, 124, 1) 100%) fixed; */
                            /* background: url('https://s3-us-w
                        est-2.amazonaws.com/s.cdpn.io/195612/coc-background.jpg') no-repeat center center fixed; */
                            /* background-size: cover;
                            font: 14px/20px "Lato", Arial, sans-serif;
                            color: #9e9e9e;
                            margin-top: 30px; */
                        }
                        .slide-container {
                            margin: auto;
                            width: fit-content;
                            text-align: center;
                        }
                        .wrapper {
                            padding-top: 40px;
                            padding-bottom: 40px;
                            float:left;
                            width:auto;
                            margin-left: 20px;
                            margin-top: 10%;
                            height:280px;
                        }
                        .wrapper:focus {
                            /* outline: 0; */
                        }
                        .clash-card {
                            background: white;
                            width: 600px;

                            height: auto;
                            display: inline-block;
                            margin: auto;
                            border-radius: 19px;
                            position: relative;
                            text-align: center;
                            box-shadow: -1px 6px 30px -6px black;
                            z-index: 9999;
                        }
                        .clash-card__image {
                            position: relative;
                            height: 230px;
                            margin-bottom: 35px;
                            border-top-left-radius: 14px;
                            border-top-right-radius: 14px;
                        }
                        .clash-card__image--barbarian {
                            background: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/195612/barbarian-bg.jpg');
                        }
                        .clash-card__image--barbarian img {
                            width: 400px;
                            position: absolute;
                            top: -65px;
                            left: -70px;
                        }
                        .clash-card__image--archer {
                            background: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/195612/archer-bg.jpg');
                        }
                        .clash-card__image--archer img {
                            width: 400px;
                            position: absolute;
                            top: -34px;
                            left: -37px;
                        }
                        .clash-card__image--giant {
                            background: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/195612/giant-bg.jpg');
                        }
                        .clash-card__image--giant img {
                            width: 340px;
                            position: absolute;
                            top: -30px;
                            left: -25px;
                        }
                        .clash-card__image--goblin {
                            background: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/195612/goblin-bg.jpg');
                        }
                        .clash-card__image--goblin img {
                            width: 370px;
                            position: absolute;
                            top: -21px;
                            left: -37px;
                        }
                        .clash-card__image--wizard {
                            background: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/195612/wizard-bg.jpg');
                        }
                        .clash-card__image--wizard img {
                            width: 345px;
                            position: absolute;
                            top: -28px;
                            left: -10px;
                        }
                        .clash-card__level {
                            text-transform: uppercase;
                            font-size: 17px;
                            font-weight:bold;
                            font-weight: auto;
                            margin-bottom: 3px;
                        }
                        .clash-card__level--barbarian {
                            color: #00a1b0;
                            /* m */
                        }

                        .clash-card__level--giant {
                            color: white;
                            font-weight: bold;
                            /* message */
                        }

                        .clash-card__unit-name {
                            font-size: 26px;
                            color: black;
                            font-weight: 900;
                            margin-bottom: 5px;
                        }
                        .clash-card__unit-description {
                            padding: 20px;
                            margin-bottom: 10px;
                        }
                        .clash-card__unit-stats--barbarian {
                            background: #00a1b0;
                            font-weight: bold;
                        }
                        .clash-card__unit-stats--barbarian .one-third {
                            border-right: 1px solid white;
                            font-weight: bold;
                        }

                        .clash-card__unit-stats--giant .one-third {
                            border-right: 1px solid white;
                            font-weight: bold;
                        }

                        .clash-card__unit-stats {
                            color: white;
                            font-weight: bold;
                            font-weight: 700;
                            border-bottom-left-radius: 14px;
                            border-bottom-right-radius: 14px;
                        }
                        .clash-card__unit-stats .one-third {
                            width: 33%;
                            float: left;
                            padding: 20px 15px;
                        }
                        .clash-card__unit-stats sup {
                            position: absolute;
                            bottom: 4px;
                            font-size: 60%;
                            font-weight: bold;
                            margin-left: 2px;
                        }
                        .clash-card__unit-stats .stat {
                            position: relative;
                            font-size: 30px;
                            margin-bottom: 10px;
                        }
                        .clash-card__unit-stats .stat-value {
                            text-transform: uppercase;
                            font-weight: 400;
                            font-size: 20px;
                            font-weight: bold;
                        }
                        .clash-card__unit-stats .no-border {
                            border-right: none;
                        }
                        .clearfix:after {
                            visibility: hidden;
                            display: block;
                            font-size: 0;
                            content: " ";
                            clear: both;
                            height: 0;
                        }
                        .slick-prev {
                            left: 100px;
                            z-index: 999;
                        }
                        .slick-next {
                            right: 100px;
                            z-index: 999;
                        }


                        .item {
                            position:relative;
                            padding-top:20px;
                            display:inline-block;
                        }
                        .notify-badge{
                            position: absolute;
                            right:9px;
                            top: -24px;
                            background:#00a1b0;
                            text-align: center;

                            font-weight: bold;
                            border-top-left-radius: 14px;
                            border-top-right-radius: 14px;
                            border-bottom-left-radius: 14px;
                            border-bottom-right-radius: 14px;

                            color:white;
                            padding:8px 10px;
                            font-size:25px;
                        }'''
