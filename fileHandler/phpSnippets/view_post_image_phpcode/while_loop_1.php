<?php
while ($row = mysqli_fetch_array($result)): ?>
             <td style="column-width: 600px;">
               <div class="row">
                 <div class="col-sm-10">
                 <hr>
                   <h4 style="text-align: center;">
                   <?php echo $row['post_name']  ?>
                  </h4>
                   <?php                     echo "<div id='img_div'>
";                   echo "<img src='http://localhost/project/Blog/User/post/post image/".$row['post_image']."'>
";                   echo "</div>
";                    ?>
                   <h4 style="text-align: center;">
                   <?php echo "-"; ?>
                   <?php echo $row['username']?>
                  </h4>
                                   </div>
               </div>
             </td>
             </tr>
           <?php endwhile;
?>