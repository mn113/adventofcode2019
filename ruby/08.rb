$data = File.open("../inputs/input08.txt", "r").each_line.first.chars
# data 0 = black
# data 1 = white
# data 2 = transparent

$width = 25
$height = 6
$period = $width * $height

# start with pre-filled transparent grid
$img = Array.new($height){Array.new($width, "2")}

$data.each_slice($period) do |layer|
    (0...$height).each do |y|
        (0...$width).each do |x|
            val = layer[$width * y + x]
            if $img[y][x] == "2"
                # write incoming pixel
                $img[y][x] = val
            else
                # as soon as a pixel is filled, pass on it
                next
            end
        end
    end
end

formatted = ""
(0...$height).each do |y|
    (0...$width).each do |x|
        formatted += $img[y][x] == '1' ? '#' : ' '
    end
    formatted += "\n"
end

printf formatted
